from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets

from users.models import Payment
from users.serializer import PaymentSerializer
from rest_framework.filters import OrderingFilter, SearchFilter


# Create your views here.
class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ('paid_lesson', 'paid_course')
    ordering_fields = ("payment_date",)
    search_fields = ('title', 'description')

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return PaymentDetailSerializer
    #     return PaymentSerializer