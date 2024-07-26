from app.domain.steps.request.simple import RequestStatusCodeStep


def test_status_code_step_should_return_success_when_run_successfully(mock_api):
    mock_api.get("http://test.com", status_code=200)
    step = RequestStatusCodeStep(
        url="http://test.com", method="GET", expected_status_code=200
    )
    step.run()
    result = step.result()
    assert result.success is True
    assert result.finished is True
    assert result.message == "Request to http://test.com returned status code 200"
    assert result.additional_information == {
        "url": "http://test.com",
        "method": "GET",
        "expected_status_code": 200,
        "status_code": 200,
    }


def test_status_code_step_should_return_success_false_when_not_succeeded(mock_api):
    mock_api.get("http://test.com", status_code=404)
    step = RequestStatusCodeStep(
        url="http://test.com", method="GET", expected_status_code=200
    )
    step.run()
    result = step.result()
    assert result.success is False
    assert result.finished is True
    assert (
        result.message
        == "Request to http://test.com returned status code 404, expected 200"
    )
    assert result.additional_information == {
        "url": "http://test.com",
        "method": "GET",
        "expected_status_code": 200,
        "status_code": 404,
    }


def test_status_code_step_should_not_return_finished_when_it_wasnt_run():
    step = RequestStatusCodeStep(
        url="http://test.com", method="GET", expected_status_code=200
    )
    result = step.result()
    assert result.success is False
    assert result.finished is False
    assert result.message == "The current step has not yet been launched."
    assert result.additional_information == {
        "url": "http://test.com",
        "method": "GET",
        "expected_status_code": 200,
    }
