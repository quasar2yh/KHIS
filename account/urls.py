from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("a_sigin/", views.AccountSiginAPIView.as_view(), name='a_sigin'),
    path("m_sigin/", views.MedicalSiginAPIView.as_view(), name='m_sigin'),
    path("logout/", views.AccountLogoutAPIView.as_view(), name="logout"),
    path("<str:username>/", views.AccountProfileAPIView.as_view(),
         name='user_read_or_update'),

]
