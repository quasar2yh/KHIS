from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import ChargeItemSerializer, ClaimSerializer
from .models import ChargeItem, Claim
# from ocs.models import ProcedureRecord, Procedure, ProcedureFee
# from ocs.serializers import ProcedureSerializer


class ChargeItemAPIView(APIView):
    def get(self, request, patient_id):
        charge = get_object_or_404(ChargeItem, id=patient_id)
        items = charge.items.all()


    # def post(self, request, patient_id):
    #     patient = get_object_or_404(Patient, id=patient_id)
    #     procedure_records = ProcedureRecord.objects.filter(patient=patient)
    #     item = ChargeItem.objects.create(
    #         name=request.data['name'],
    #         quantity=request.data['quantity'],
    #         price=request.data['price']
    #     )
    #     return Response({'message': 'Item created successfully'}, status=status.HTTP_201_CREATED)
    
