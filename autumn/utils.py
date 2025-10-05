import random
from typing import Any, Callable, Dict, Set, Type, TypeVar

from pydantic import BaseModel, ValidationError

from .error import AutumnHTTPError, AutumnValidationError

T = TypeVar("T", bound=BaseModel)


def _snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def _decompose_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, (list, tuple, set)):
        return [_decompose_value(item) for item in value]

    return value


def _build_payload(
    scope: Dict[str, Any], method: Callable, *, ignore: Set[str] = set()
) -> Dict[str, Any]:
    params = method.__code__.co_varnames
    camel_case_params = [_snake_to_camel(p) for p in params]
    payload: Dict[str, Any] = {}

    for key, value in scope.items():
        payload_param = key
        if payload_param in camel_case_params:
            index = camel_case_params.index(payload_param)
            payload_param = params[index]

        if (
            payload_param != "self"
            and (payload_param in params)
            and (payload_param not in ignore)
            and (value is not None)
        ):
            payload[payload_param] = _decompose_value(value)

    return payload


def _build_model(model: Type[T], data: Dict[str, Any]) -> T:
    try:
        return model.model_validate(data)
    except ValidationError as e:
        errors = e.errors()
        error_message = errors[0]["msg"]
        error_path = errors[0]["loc"]
        error_code = errors[0]["type"]

        err = AutumnValidationError(
            f"{error_message} at {error_path} with code {error_code}",
            "validation_error",
        )
        err.add_note("Received response: " + str(data))
        raise err


def _check_response(status_code: int, data: Dict[str, Any]) -> None:
    if not 200 <= status_code < 300:
        message = data.get("message", "No error message provided.")
        code = data.get("code", "unknown_error")
        raise AutumnHTTPError(
            message,
            code,
            status_code,
        )


class ExponentialBackoff:
    def __init__(self):
        rand = random.Random()
        rand.seed()

        self._rand = rand
        self._base = 2
        self._state = 0

    def tick(self):
        self._state += 1

    @property
    def bedtime(self):
        raw_time = self._base**self._state
        jitter = self._rand.uniform(0, 1)
        return raw_time + jitter
