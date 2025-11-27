# Python ML microservice
FROM python:3.10-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY ml-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ml-service/ .
# If you have a model artifact, COPY it here:
# COPY ml-service/model_artifacts /app/model_artifacts
EXPOSE 8000
# Example: uvicorn FastAPI app in ml-service/app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
