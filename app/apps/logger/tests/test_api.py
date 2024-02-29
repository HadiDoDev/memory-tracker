from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_memory_logs():
    # Send a GET request to /memory-logs/
    response = client.get("/memory-logs/")

    # Check status code
    assert response.status_code == 200

    # Check response content
    logs = response.json()
    assert isinstance(logs, list)

    # Checking the content of each element in the list
    for log in logs:
        assert "timestamp" in log
        assert "total" in log
        assert "free" in log
        assert "used" in log
