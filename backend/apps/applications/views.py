from rest_framework import generics, status
from rest_framework.response import Response
from .models import CreditApplication
from .serializers import CreditApplicationSerializer
from django.conf import settings
import requests

class CreditApplicationListCreateView(generics.ListCreateAPIView):
    queryset = CreditApplication.objects.all().order_by("-created_at")
    serializer_class = CreditApplicationSerializer

    def perform_create(self, serializer):
        # create application first
        instance = serializer.save()
        # Optionally call ML service to score the application
        ml_url = getattr(settings, "ML_SERVICE_URL", None)
        if ml_url:
            try:
                payload = {
                    "id": instance.id,
                    "income": instance.income,
                    "age": instance.age,
                    "credit_history_score": instance.credit_history_score,
                    "requested_amount": instance.requested_amount,
                }
                resp = requests.post(f"{ml_url.rstrip('/')}/score", json=payload, timeout=5)
                if resp.ok:
                    data = resp.json()
                    instance.risk_score = data.get("risk_score")
                    instance.is_processed = True
                    instance.save()
            except Exception:
                # dont block creation if ML service fails
                pass
