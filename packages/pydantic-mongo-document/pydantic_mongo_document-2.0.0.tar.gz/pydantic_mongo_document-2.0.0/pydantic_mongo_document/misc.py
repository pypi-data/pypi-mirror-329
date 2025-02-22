import asyncio
from typing import Awaitable, Callable, ParamSpec, TypeVar

from pydantic import BaseModel

T = TypeVar("T")
R = TypeVar("R")
P = ParamSpec("P")


def find_generic_origin(model: type[BaseModel]):
    """Find generic origin of a model."""

    for base in model.__bases__:
        if not hasattr(base, "__pydantic_generic_metadata__"):
            continue

        origin = base.__pydantic_generic_metadata__.get("origin")

        if origin is not None:
            return origin, base

        origin, base = find_generic_origin(base)

        if origin is not None:
            return origin, base

    return None, None


def get_model_generic_value(
    model: type[BaseModel],
    parameter: T,
    raise_exc: bool = True,
) -> type[T]:
    """Get generic arguments value of a model."""

    origin, base = find_generic_origin(model)

    origin_type_vars = origin.__pydantic_generic_metadata__["parameters"]

    for i, arg in enumerate(origin_type_vars):
        if arg == parameter:
            return base.__pydantic_generic_metadata__["args"][i]

    if raise_exc:
        raise ValueError(f"Parameter {parameter} not found in model {model} generic arguments.")


def async_wrap(result: Awaitable[T] | T, func: Callable[[T], R]) -> Awaitable[R] | R:
    """Wrap function to be async."""

    async def wrapper(coro: Awaitable[T]) -> R:
        return func(await coro)

    return wrapper(result) if asyncio.iscoroutine(result) else func(result)
