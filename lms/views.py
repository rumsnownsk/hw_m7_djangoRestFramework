#views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from lms.serializer import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner, NotModer

from .models import Course, Lesson

class LessonListCreateAPIView(generics.ListCreateAPIView):
    """GET список уроков + POST создание"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = {
        # /lessons/?course__isnull=true
        'course': ['exact', 'isnull'],
        'owner': ['exact', 'isnull']
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAuthenticated, NotModer]
        else:
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]


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


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курсов: list, retrieve, create, update, destroy"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
