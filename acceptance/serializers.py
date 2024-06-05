from rest_framework import serializers
from .models import Claim, ChargeItem
from ocs.serializers import ProcedureRecordSerializer

class ChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = '__all__'


class ClaimSerializer(serializers.ModelSerializer):
    charge_items = serializers.PrimaryKeyRelatedField(many=True, queryset=ChargeItem.objects.all())
    procedure_record = ProcedureRecordSerializer()
    class Meta:
        model = Claim
        fields = '__all__'
        extra_kwargs = {
            'charge_items': {'read_only': True},
            'procedure': {'read_only': True},
            'procedure_record': {'read_only': True}
        }




