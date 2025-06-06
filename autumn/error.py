from typing import Any, Self

__all__ = ("AutumnError", "AutumnValidationError")


class AutumnError(Exception):
    """
    Base exception for all Autumn errors.

    Attributes
    ----------
    message: str
        The error message.
    code: str
        The error code.
    """

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message}, {self.code})"


class AutumnValidationError(AutumnError):
    """
    Exception raised when a validation error occurs.
    This is raised when the API returns a response that isn't recognized by the library.

    Attributes
    ----------
    message: str
        The error message.
    code: str
        The error code.
    """

    def __init__(self, message: str, code: str):
        super().__init__(message, code)


class AutumnHTTPError(AutumnError):
    """
    Exception raised when an HTTP error occurs.

    Attributes
    ----------
    message: str
        The error message. This can be an empty string.
    code: str
        The error code.
    status_code: int
        The HTTP status code.
    """

    def __init__(self, message: str, code: str, status_code: int):
        super().__init__(message, code)
        self.status_code = status_code

        self.body = ""

    def __str__(self):
        return f"{self.code}: {self.message} (HTTP {self.status_code})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message}, {self.code}, {self.status_code})\n{self.body}"

    def attach_body(self, body: Any) -> Self:
        self.body = body
        return self
