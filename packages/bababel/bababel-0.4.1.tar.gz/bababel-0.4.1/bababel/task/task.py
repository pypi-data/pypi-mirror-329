import inspect
import re
from abc import ABC, abstractmethod

from bababel import Consumer
from bababel.bababel_app import BababelApp
from bababel.exceptions.base_bababel_error import TaskError


class Task(ABC):  # find a way for this to be sigleton or other thing that works
    """
    Abstract base class for defining asynchronous tasks.

    This class enforces the structure for task execution by requiring subclasses
    to implement the `run` method and define a `app` attribute.

    Example:
        Creating and executing a task:

        class HelloWorld(Task)
            def run(*args, **kwargs):
                print('Hello World')

        task = HelloWorld(app="example")
        task.run(*args, **kwargs)

        Alternatively, you can call the task instance directly:

        task(*args, **kwargs)

    Attributes:
        name (str): The class name, set dynamically. It is also the identifier of the task and must be unique.
    """

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of a Task subclass.
        """
        instance = super().__new__(cls)
        cls.name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()  # Converts to snake case
        # TODO: make a utils function

        return instance

    def __init__(self, app: BababelApp, consumer=Consumer):
        """
        Args:
            app (BababelApp): The app to be assigned to the instance.
            consumer (Consumer): The consumer that will process the tasks.
        """
        self.app = app
        self.consumer = consumer

    @abstractmethod
    def run(self, *args, **kwargs):
        """The main process of the task."""
        raise NotImplementedError()

    def send(self, *args, **kwargs):
        self._inspect_arguments(*args, **kwargs)
        self.app.publisher.publish(task_name=self.name, body=self._get_body(*args, **kwargs))

    def _inspect_arguments(self, *args, **kwargs):
        sig = inspect.signature(self.run)
        try:
            sig.bind(*args, **kwargs)
        except TypeError as e:
            # Build a string for the expected parameters and their annotations
            expected_params = ', '.join(
                f"{name}: {param.annotation.__name__}"
                for name, param in sig.parameters.items()
            )
            # Build a string for the received positional args
            received_args = ', '.join(
                f"{name}: {value}"
                for name, value in zip(sig.parameters, args)
            )
            # Build a string for the received keyword args
            received_kwargs = ', '.join(
                f"{key}: {value}"
                for key, value in kwargs.items()
            )
            # Raise an error with a clear diagnostic message
            raise TaskError(
                "Invalid arguments: "
                f"Expected (parameters: {expected_params}), "
                f"got (args: {received_args}, kwargs: {received_kwargs})"
            ) from e

    def _get_body(self, *args, **kwargs):
        param_names = list(inspect.signature(self.__class__.run).parameters.keys())[1:]
        args_dict = {name: value for name, value in zip(param_names, args)}
        args_dict.update(kwargs)
        return args_dict
