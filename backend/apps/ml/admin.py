from django.contrib import admin
from .models import ModelRun

@admin.register(ModelRun)
class ModelRunAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "created_at")
    readonly_fields = ("created_at",)
