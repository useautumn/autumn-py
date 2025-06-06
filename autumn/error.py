from typing import Any, Self

__all__ = ("AutumnError", "AutumnValidationError")


class AutumnError(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message}, {self.code})"


class AutumnValidationError(AutumnError):
    def __init__(self, message: str, code: str):
        super().__init__(message, code)


class AutumnHTTPError(AutumnError):
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
