from rest_framework import serializers
from .models import Annual,HospitalSchedule
from account.models import Practitioner


class AnnualSerializer(serializers.ModelSerializer):
    practitioner_id = serializers.PrimaryKeyRelatedField(
        source='practitioner', read_only=True)

    class Meta:
        model = Annual
        fields = ['practitioner_id', 'start_date', 'end_date', 'reason']
        
        
        
        
class HospitalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalSchedule
        fields = ['id', 'date', 'date_name', 'is_hospital_holiday','is_public_holiday' ]
