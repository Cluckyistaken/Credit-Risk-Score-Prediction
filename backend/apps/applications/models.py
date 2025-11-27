from django.db import models
from django.conf import settings

class CreditApplication(models.Model):
    """
    Represents a single credit application for scoring.
    Add fields that are important for credit scoring.
    """
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    income = models.FloatField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    credit_history_score = models.FloatField(null=True, blank=True)
    requested_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    risk_score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.requested_amount}"
