from rest_framework import serializers
from .models import Annual, HospitalSchedule,AnnualLeave,DepartmentEvent
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
        fields = ['id', 'date', 'date_name',
                  'is_hospital_holiday', 'is_public_holiday']


class MailSerializer(serializers.Serializer):  # 이메일
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


class DepartmentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentEvent
        fields = ['id', 'department', 'event_title',
                  'event_content', 'start_time', 'end_time']


class AnnualLeaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnualLeave
        fields = ['practitioner', 'annual_leave_count', 'leave_taken', 'remaining_leave']