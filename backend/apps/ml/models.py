from django.db import models

class ModelRun(models.Model):
    """
    Keeps a very small log of ML scoring runs (optional).
    """
    external_id = models.CharField(max_length=255, blank=True, null=True)
    payload = models.JSONField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Run {self.id}"
