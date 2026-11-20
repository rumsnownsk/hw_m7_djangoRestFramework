from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.serializer import PaymentSerializer, UserSerializer


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
    # permission_classes = (AllowAny,)

    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     user.set_password(user.password)
    #     user.save()

class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user