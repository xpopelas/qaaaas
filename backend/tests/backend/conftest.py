import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture
def app_test_client():
    with TestClient(app) as client:
        yield client
