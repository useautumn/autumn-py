class AutumnError(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.code}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message}, {self.code})"
