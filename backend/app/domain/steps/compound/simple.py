from app.domain.steps.base import AbstractStep, StepResult


class CompoundStep(AbstractStep):
    def __init__(self, steps: list[AbstractStep]):
        """Step for running multiple steps together chained.
        Returns the result of success, or first encountered failure.

        :param steps: AbstractStep steps that should be run in that sequence.
        """
        self._steps = steps
        self._step_results = []
        self._result = StepResult()

    def _compose_additional_information(self) -> dict:
        """Composes additional information for the result of the compound step.

        :return: Additional information for the result of the compound step.
        """
        return {
            "steps_results": [
                {
                    "success": step_result.success,
                    "finished": step_result.finished,
                    "message": step_result.message,
                    "additional_information": step_result.additional_information,
                }
                for step_result in self._step_results
            ]
        }

    def run(self) -> None:
        if not self._steps:
            self._result = StepResult(
                finished=True,
                success=True,
                message="Compound step has no steps to run",
                additional_information={},
            )
            return

        for index, step in enumerate(self._steps):
            step.run()
            result = step.result()
            self._step_results.append(result)
            if not result.success:
                self._result = StepResult(
                    finished=True,
                    success=False,
                    message=f"Step {index + 1} failed",
                    additional_information=self._compose_additional_information(),
                )
                return

        self._result = StepResult(
            finished=True,
            success=True,
            message="Compound test passed",
            additional_information=self._compose_additional_information(),
        )

    def result(self) -> StepResult:
        return self._result
