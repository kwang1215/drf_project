from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

from accounts.views import (
    LogoutAPIView,
    UserProfileUpdateAPIView,
    PasswordChangeAPIView,
    UserManageAPIView,
)


urlpatterns = [
    path("", UserManageAPIView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("<str:username>/", views.UserProfileAPIView.as_view(), name="profile"),
    path(
        "<str:username>/update/",
        UserProfileUpdateAPIView.as_view(),
        name="profile_update",
    ),
    path("password/", PasswordChangeAPIView.as_view(), name="password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
