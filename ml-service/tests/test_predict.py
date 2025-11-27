# ml-service/tests/test_predict.py
import json
import os
import pytest
from fastapi.testclient import TestClient

from app import app, pipeline

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert "status" in body
    assert body["status"] == "ok"

@pytest.mark.skipif(pipeline is None, reason="Model pipeline not loaded; run training first")
def test_predict_single():
    sample = {
        "age": 30,
        "income": 50000,
        "loan_amount": 8000,
        "employment_status": "employed",
        "credit_history": "good"
    }
    resp = client.post("/predict_single", json={"__root__": sample})
    assert resp.status_code == 200
    body = resp.json()
    assert "prediction" in body
    assert "probability" in body

@pytest.mark.skipif(pipeline is None, reason="Model pipeline not loaded; run training first")
def test_predict_batch():
    payload = {
        "data": [
            {
                "age": 30,
                "income": 50000,
                "loan_amount": 8000,
                "employment_status": "employed",
                "credit_history": "good"
            },
            {
                "age": 28,
                "income": 28000,
                "loan_amount": 6000,
                "employment_status": "student",
                "credit_history": "bad"
            }
        ]
    }
    resp = client.post("/predict", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert "predictions" in body
    assert isinstance(body["predictions"], list)
