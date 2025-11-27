from django.urls import path
from .views import CreditApplicationListCreateView

urlpatterns = [
    path("", CreditApplicationListCreateView.as_view(), name="application-list-create"),
]
