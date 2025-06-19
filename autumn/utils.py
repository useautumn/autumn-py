from typing import Dict, Any, Callable, Type, TypeVar, Set

from pydantic import BaseModel, ValidationError

from .error import AutumnValidationError, AutumnHTTPError


T = TypeVar("T", bound=BaseModel)


def _decompose_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, list):
        return [_decompose_value(item) for item in value]

    return value


def _build_payload(
    scope: Dict[str, Any], method: Callable, *, ignore: Set[str] = set()
) -> Dict[str, Any]:
    params = method.__code__.co_varnames
    payload: Dict[str, Any] = {}

    for key, value in scope.items():
        if key != "self" and key in params and key not in ignore and value is not None:
            payload[key] = _decompose_value(value)

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
