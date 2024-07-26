import abc
import dataclasses


@dataclasses.dataclass
class StepResult:
    """Dataclass for storing the result of a step.

    :param finished: Whether the step has finished (returns false if the step is still running or has not been started yet)
    :param success: Whether the step was successful
    :param message: A message describing the result
    :param additional_information: Additional information about the result
    """

    finished: bool = False
    success: bool = False
    message: str = "The current step has not yet been launched."
    additional_information: dict = dataclasses.field(default_factory=dict)


class AbstractStep(abc.ABC):
    @abc.abstractmethod
    def run(self) -> None:
        """Method for running a singular runnable step.

        :return: Nothing
        """
        raise NotImplementedError

    @abc.abstractmethod
    def result(self) -> StepResult:
        """Method for getting the result of a step.

        :return: StepResult describing the result of the step
        """
        raise NotImplementedError
