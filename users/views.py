from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.permissions import IsCurrentUser
from users.serializer import PaymentSerializer, UserSerializer, UserShortSerializer


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

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
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









