from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import *

app_name = LmsConfig.name


router = DefaultRouter()
# ViewSet из под капота предоставляет комплекс CRUD-операций
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailAPIView.as_view(), name="lesson-detail"),
] + router.urls
