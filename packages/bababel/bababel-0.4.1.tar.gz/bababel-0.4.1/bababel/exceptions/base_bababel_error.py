class BababelError(Exception):
    """Base exception class for this lib,"""

    def __init__(self, message: str = None, code: str = None, details: str = None):
        self.message = message
        self.code = code
        self.details = details


class TaskError(BababelError):
    pass
