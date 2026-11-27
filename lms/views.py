# views.py
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.serializer import *
from users.permissions import IsModer, IsOwner, NotModer

from .models import Course, Lesson, Subscription
from .paginations import CustomPagination


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """GET список уроков + POST создание"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        # /lessons/?course__isnull=true
        "course": ["exact", "isnull"],
        "owner": ["exact", "isnull"],
    }
    pagination_class = CustomPagination

    def get_queryset(self):
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, NotModer]
        else:
            self.permission_classes = [
                IsAuthenticated,
            ]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return LessonSerializer
        return LessonShortSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH"):
            # править может модератор ИЛИ владелец
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.request.method in ("DELETE",):
            # удалять может только владелец, модераторам нельзя
            self.permission_classes = (IsAuthenticated, NotModer, IsOwner)
        else:
            # GET
            self.permission_classes = (IsAuthenticated,)
        return [permission() for permission in self.permission_classes]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="description from swagger_auto_schema via method_decorator"
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов: list, retrieve, create, update, destroy"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, NotModer)
        elif self.action in ("update", "partial_update"):
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner)
        elif self.action in ("destroy",):
            # удалять может только владелец, модераторам нельзя
            self.permission_classes = (IsAuthenticated, NotModer, IsOwner)
        else:
            # GET
            self.permission_classes = (IsAuthenticated,)
            # pass
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return CourseSerializer
        return CourseShortSerializer


class SubscriptionToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        course = get_object_or_404(Course, pk=pk)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course_id=pk)
            message = "Подписка добавлена"

        return Response({"message": message})
