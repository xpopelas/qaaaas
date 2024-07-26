from app.domain.steps.base import StepResult
from app.domain.steps.compound.simple import CompoundStep


def test_compound_step_reports_success_without_any_step():
    uut = CompoundStep(steps=[])
    uut.run()
    result = uut.result()
    assert result.success is True
    assert result.finished is True
    assert result.message == "Compound step has no steps to run"
    assert result.additional_information == {}


def test_compound_step_reports_failure_as_unsuccessful(simple_step_factory):
    step_1 = simple_step_factory(
        StepResult(success=False, finished=True, message="I have failed")
    )
    uut = CompoundStep(steps=[step_1])
    uut.run()
    result = uut.result()
    assert result.success is False
    assert result.finished is True
    assert result.message == "Step 1 failed"
    assert result.additional_information == {
        "steps_results": [
            {
                "success": False,
                "finished": True,
                "message": "I have failed",
                "additional_information": {},
            }
        ]
    }


def test_compound_step_reports_success_as_successful(simple_step_factory):
    step_1 = simple_step_factory(
        StepResult(success=True, finished=True, message="I have succeeded")
    )
    uut = CompoundStep(steps=[step_1])
    uut.run()
    result = uut.result()
    assert result.success is True
    assert result.finished is True
    assert result.message == "Compound test passed"
    assert result.additional_information == {
        "steps_results": [
            {
                "success": True,
                "finished": True,
                "message": "I have succeeded",
                "additional_information": {},
            }
        ]
    }


def test_compound_step_stops_at_first_failure(simple_step_factory):
    step_1 = simple_step_factory(
        StepResult(success=True, finished=True, message="I have passed")
    )
    step_2 = simple_step_factory(
        StepResult(success=False, finished=True, message="I have failed")
    )
    step_3 = simple_step_factory(
        StepResult(success=True, finished=True, message="I could pass, but wasn't run")
    )
    uut = CompoundStep(steps=[step_1, step_2, step_3])
    uut.run()
    result = uut.result()
    assert result.success is False
    assert result.finished is True
    assert result.message == "Step 2 failed"
    assert result.additional_information == {
        "steps_results": [
            {
                "success": True,
                "finished": True,
                "message": "I have passed",
                "additional_information": {},
            },
            {
                "success": False,
                "finished": True,
                "message": "I have failed",
                "additional_information": {},
            },
        ]
    }


def test_compound_test_succeeds_even_after_multiple_tests(simple_step_factory):
    step_1 = simple_step_factory(
        StepResult(success=True, finished=True, message="I have passed")
    )
    step_2 = simple_step_factory(
        StepResult(
            success=True,
            finished=True,
            message="I have also passed",
            additional_information={"test_key": "gets passed"},
        )
    )
    step_3 = simple_step_factory(
        StepResult(success=True, finished=True, message="I have passed as last")
    )
    uut = CompoundStep(steps=[step_1, step_2, step_3])
    uut.run()
    result = uut.result()
    assert result.success is True
    assert result.finished is True
    assert result.message == "Compound test passed"
    assert result.additional_information == {
        "steps_results": [
            {
                "success": True,
                "finished": True,
                "message": "I have passed",
                "additional_information": {},
            },
            {
                "success": True,
                "finished": True,
                "message": "I have also passed",
                "additional_information": {"test_key": "gets passed"},
            },
            {
                "success": True,
                "finished": True,
                "message": "I have passed as last",
                "additional_information": {},
            },
        ]
    }
