from typing import Dict, Any, Callable, Type, TypeVar, Set

from pydantic import BaseModel, ValidationError

from .error import AutumnValidationError


T = TypeVar("T", bound=BaseModel)


def _build_payload(
    scope: Dict[str, Any], method: Callable, *, ignore: Set[str] = set()
) -> Dict[str, Any]:
    params = method.__code__.co_varnames
    payload: Dict[str, Any] = {}

    for key, value in scope.items():
        if key != "self" and key in params and key not in ignore:
            payload[key] = value.model_dump() if isinstance(value, BaseModel) else value

    return payload


def _build_model(model: Type[T], data: Dict[str, Any]) -> T:
    try:
        return model.model_validate(data)
    except ValidationError as e:
        errors = e.errors()
        error_message = errors[0]["msg"]
        error_path = errors[0]["loc"]
        error_code = errors[0]["type"]

        raise AutumnValidationError(
            f"{error_message} at {error_path} with code {error_code}",
            "validation_error",
        )
