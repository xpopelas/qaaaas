import pytest
import requests_mock
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture
def app_test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m
