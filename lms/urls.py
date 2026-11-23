from django.urls import path
from rest_framework.routers import DefaultRouter

from lms.apps import LmsConfig
from lms.views import *
from users.views import PaymentListAPIView

app_name = LmsConfig.name


router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieveUpdateDestroyAPIView.as_view(), name="lesson-detail"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),

    path("courses/<int:pk>/subscribe-toggle/", SubscriptionToggleAPIView.as_view(), name="subscribe-toggle")
] + router.urls
