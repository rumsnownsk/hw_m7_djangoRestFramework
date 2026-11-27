from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from users.models import Payment, User
from users.permissions import IsCurrentUser
from users.serializer import PaymentSerializer, UserSerializer, UserShortSerializer
from users.servises import (
    convert_rub_to_dollars,
    create_stripe_price,
    create_stripe_session,
    create_stripe_product,
    checkout_stripe_payment,
)
from rest_framework.response import Response


# Create your views here.
class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ("paid_lesson", "paid_course")
    ordering_fields = ("payment_date",)
    search_fields = ("title", "description")

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return PaymentDetailSerializer
    #     return PaymentSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCurrentAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        # Мы сами говорим: «объект — это request.user»
        return self.request.user


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            self.permission_classes = (IsAuthenticated, IsCurrentUser)
        else:
            self.permission_classes = (IsAuthenticated,)

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        pk = self.kwargs.get(self.lookup_field)  # pk из URL, строка
        user = self.request.user
        if pk and user.is_authenticated and int(pk) == user.pk:
            return UserSerializer  # свой профиль — полный вид
        return UserShortSerializer  # чужой — укороченный


class PaymentCreateAPIView(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        # amount_in_dollars = convert_rub_to_dollars(payment.amount)

        product = create_stripe_product(payment.get_paid_object())
        price = create_stripe_price(payment, product)

        session_id, payment_link = create_stripe_session(price)

        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class PaymentStatusAPIView(APIView):

    def get(self, request, pk):
        payment = get_object_or_404(Payment, pk=pk, user=request.user)

        if payment.status != "paid":
            info = checkout_stripe_payment(payment.session_id)
            if info.payment_status == "paid":
                payment.status = "paid"
                payment.payment_date = timezone.now()
                payment.save()
        return Response(
            {
                "payment_id": payment.pk,
                "status": payment.status,
            }
        )
