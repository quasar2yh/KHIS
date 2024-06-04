from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProcedureAPIView.as_view()),
    path('<int:procedure_id>/', views.ProcedureDetailAPIView.as_view()),
]