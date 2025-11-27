from rest_framework import serializers
from .models import CreditApplication

class CreditApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditApplication
        fields = "__all__"
        read_only_fields = ("id", "created_at", "risk_score", "is_processed")
