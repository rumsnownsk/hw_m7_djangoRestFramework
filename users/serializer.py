from rest_framework.serializers import SerializerMethodField, ModelSerializer

from .models import Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



