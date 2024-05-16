from rest_framework import serializers

class AnnualSerializer(serializers.Serializer):
    date = serializers.DateField()
