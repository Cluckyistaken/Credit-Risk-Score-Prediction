from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ModelRunSerializer
from .models import ModelRun
from .services import MLService

class CreditRiskScoreView(APIView):
    """
    Real ML endpoint using the Antigravity model.
    """
    def post(self, request):
        data = request.data or {}
        
        try:
            # Use the ML Service to get prediction
            result = MLService.predict(data)
            
            risk_score = result.get("probability", 0.0)
            if risk_score is None:
                # Fallback if probability not available, use prediction (0 or 1)
                risk_score = float(result["prediction"])
            
            # Save a record
            run = ModelRun.objects.create(payload=data, result=result)
            
            return Response({
                "risk_score": risk_score, 
                "prediction": result["prediction"],
                "run_id": run.id
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
