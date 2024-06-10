from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProcedureFeeCreateListAPIView.as_view()),
    path('<int:procedurefee_id>/', views.ProcedureFeeDetailAPIView.as_view()),
]