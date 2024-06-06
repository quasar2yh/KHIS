from rest_framework import serializers
from .models import Claim, ChargeItem
from ocs.serializers import ProcedureRecordSerializer
from account.serializers import PatientSerializer
from account.models import Patient


class ChargeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargeItem
        fields = '__all__'


class NestedChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('claim', None)
        representation.pop('patient', None)
        return representation
    

class ClaimSerializer(serializers.ModelSerializer):
    charge_items = NestedChargeItemSerializer(many=True, read_only=True)

    class Meta:
        model = Claim
        fields = '__all__'

    


class PatientChargeItemSerializer(serializers.ModelSerializer):
    charge_items = ChargeItemSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class PatientClaimSerializer(serializers.ModelSerializer):
    claims = ClaimSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'