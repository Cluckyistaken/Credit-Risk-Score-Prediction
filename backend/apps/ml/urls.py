from django.urls import path
from .views import CreditRiskScoreView

urlpatterns = [
    path('score', CreditRiskScoreView.as_view(), name='ml_score'),
]
