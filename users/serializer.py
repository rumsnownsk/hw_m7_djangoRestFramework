from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.serializer import LessonShortSerializer, CourseShortSerializer
from .models import Payment, User
from .permissions import IsModer


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserShortSerializer(ModelSerializer):
    lessons = LessonShortSerializer(many=True, read_only=True)
    courses = CourseShortSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # password включаем в fields, а exclude убираем совсем
        fields = ["id", "email", "city", "avatar", "lessons", "courses"]


class UserSerializer(ModelSerializer):
    is_moder = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(many=True, read_only=True)
    courses = CourseShortSerializer(many=True, read_only=True)

    class Meta:
        model = User
        # password включаем в fields, а exclude убираем совсем
        fields = ["id", "email", "password", "phone", "city", "avatar", "is_moder", "lessons", "courses"]
        extra_kwargs = {"password": {"write_only": True}}

    def get_is_moder(self, obj):
        #!!!!!!!!! obj — это уже пользователь. !!!!!!!!!!
        if obj.groups.filter(name='moders').exists():
            return "Модератор"
        return None


    def create(self, validated_data):
        # print("VALIDATED_DATA:", validated_data)  # смотри в консоль сервера или shell
        user = User.objects.create_user(**validated_data)
        # print("SAVED PASSWORD:", user.password)  # хеш или пустота?
        return user


