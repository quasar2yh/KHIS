from rest_framework import serializers
from .models import Claim, ChargeItem, ProcedureFee
# from ocs.models import Procedure, ProcedureRecord
# from ocs.serializers import ProcedureSerializer, ProcedureRecordSerializer

class ChargeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeItem
        fields = '__all__'


# class ClaimSerializer(serializers.ModelSerializer):
#     charge_items = serializers.PrimaryKeyRelatedField(many=True, queryset=ChargeItem.objects.all())
#     procedure = ProcedureSerializer()
#     procedure_record = ProcedureRecordSerializer()
#     class Meta:
#         model = Claim
#         fields = '__all__'
#         extra_kwargs = {
#             'charge_items': {'read_only': True},
#             'procedure': {'read_only': True},
#             'procedure_record': {'read_only': True}
#         }


class ProcedureFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcedureFee
        fields = '__all__'


