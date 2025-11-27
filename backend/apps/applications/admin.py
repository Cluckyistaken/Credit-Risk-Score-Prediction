from django.contrib import admin
from .models import CreditApplication

@admin.register(CreditApplication)
class CreditApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "applicant", "requested_amount", "risk_score", "is_processed", "created_at")
    list_filter = ("is_processed",)
    search_fields = ("name",)
