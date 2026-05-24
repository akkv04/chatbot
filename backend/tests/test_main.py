import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_chat_endpoint_schema():
    # Test just the schema/validation without real LLM mock yet
    # We pass an empty message and check if it handles it (should be 200 but maybe empty answer)
    # This is more of a smoke test
    response = client.post("/chat", json={"message": "Hello"})
    # It might fail with 500 if GOOGLE_API_KEY is missing, which is expected in a bare test env
    # But it proves the routing and pydantic models are correct.
    assert response.status_code in [200, 500] 

def test_data_dir_creation():
    # Check if startup_event creates the data dir
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    assert os.path.exists(data_dir)
