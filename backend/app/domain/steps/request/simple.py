import requests

from app.domain.steps.base import AbstractStep, StepResult


class RequestStatusCodeStep(AbstractStep):
    def __init__(
        self,
        url: str,
        method: str,
        expected_status_code: int,
    ):
        """Step for checking the status code of a request.
        Any step regardless of its success or run will return the same parameters in additional_info of result call.

        :param url: URL to send a request to
        :param method: Method with which we want to send the status code
        :param expected_status_code: What status code we expect to receive
        """
        self._url = url
        self._method = method
        self._expected_status_code = expected_status_code
        self._result = StepResult(
            additional_information=self._default_additional_information()
        )

    def _default_additional_information(self) -> dict:
        """Returns the base additional information for the step.

        :return: default object containing called parameters
        """
        return {
            "url": self._url,
            "method": self._method,
            "expected_status_code": self._expected_status_code,
        }

    def run(self) -> None:
        response = requests.request(method=self._method, url=self._url)
        if response.status_code == self._expected_status_code:
            self._result = StepResult(
                finished=True,
                success=True,
                message=f"Request to {self._url} returned status code {self._expected_status_code}",
                additional_information={
                    "status_code": response.status_code,
                    **self._default_additional_information(),
                },
            )
        else:
            self._result = StepResult(
                finished=True,
                success=False,
                message=f"Request to {self._url} returned status code {response.status_code}, expected {self._expected_status_code}",
                additional_information={
                    "status_code": response.status_code,
                    **self._default_additional_information(),
                },
            )

    def result(self) -> StepResult:
        return self._result
