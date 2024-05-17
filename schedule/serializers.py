from rest_framework import serializers
from .models import Annual
from account.models import Practitioner


class AnnualSerializer(serializers.ModelSerializer):
    practitioner_id = serializers.PrimaryKeyRelatedField(
        source='practitioner', read_only=True)

    class Meta:
        model = Annual
        fields = ['practitioner_id', 'start_date', 'end_date', 'reason']
