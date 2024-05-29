from django.urls import path
from . import views

urlpatterns = [
    path('', views.PractitionerAPIView.as_view()),
    path('<int:practitioner_id>/', views.PractitionerAPIView.as_view()),
]