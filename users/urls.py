from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import *

app_name = UsersConfig.name

urlpatterns = [
    path(
        "",
        UserListAPIView.as_view(),
        name="users-list",
    ),
    path(
        "register/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("current/", UserCurrentAPIView.as_view(), name="current-user"),
    path("<int:pk>/", UserRetrieveUpdateDestroyAPIView.as_view(), name="detail-user"),
    path("payment/", PaymentCreateAPIView.as_view(), name="payment"),
    path(
        "payment/<int:pk>/status/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
]
