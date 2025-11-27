from rest_framework import serializers
from .models import ModelRun

class ModelRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelRun
        fields = "__all__"
