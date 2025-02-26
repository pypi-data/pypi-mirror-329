from dataclasses import dataclass
from typing import Callable


@dataclass
class QueueCallbackBind:
    """
    A data class that binds a queue name to a callback function.

    Attributes:
        queue (str): The name of the queue.
        callback (Callable): A function that is called when an event occurs on the queue.
    """
    queue: str
    callback: Callable
