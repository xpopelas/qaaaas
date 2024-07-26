from typing import Callable

import pytest
import requests_mock
from starlette.testclient import TestClient

from app.domain.steps.base import AbstractStep, StepResult
from app.main import app


@pytest.fixture
def app_test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_api():
    with requests_mock.Mocker() as m:
        yield m


class SimpleTestStep(AbstractStep):
    def __init__(self, result: StepResult):
        self._result = result
        self.was_run = False

    def run(self) -> None:
        self.was_run = True

    def result(self):
        return self._result


@pytest.fixture
def simple_step_factory() -> Callable[[StepResult], SimpleTestStep]:
    def factory(result: StepResult):
        return SimpleTestStep(result)

    return factory
