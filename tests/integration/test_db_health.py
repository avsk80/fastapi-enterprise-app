import os
import httpx
import pytest

@pytest.mark.integration
def test_health_db_ok():
    base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")
    r = httpx.get(f"{base_url}/health/db", timeout=5)
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}