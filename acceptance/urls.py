from django.urls import path
from . import views

urlpatterns = [path("charge-item/<int:charge_item_id>/", views.ChargeItemDetailAPIView.as_view(), name="charge_item_detail"),
               path("charge-item/", views.ChargeItemCreateAPIView.as_view(), name="charge_item_create"),
               path("claim/patient/", views.PatientClaimCreateListAPIView.as_view(), name="patient_claim_create_list"),
               path("claim/<int:claim_id>/", views.PatientClaimDetailAPIView.as_view(), name="patient_claim_detail"),
               path("claim/", views.ClaimListAPIView.as_view(), name="claim_list"),
               ]