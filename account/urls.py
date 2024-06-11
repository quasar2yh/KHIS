from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.CookieTokenObtainPairView.as_view()),
    path('logout/', views.LogoutApi.as_view()),
    path("token/refresh/", views.CookieTokenRefreshView.as_view()),
    path("register/", views.AccountSiginAPIView.as_view()),
    path("<int:account_id>/", views.AccountSiginAPIView.as_view()),
    path("pwchange/<int:account_id>/", views.ChangePasswordAPIView.as_view()),
]
