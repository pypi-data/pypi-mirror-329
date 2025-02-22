import typing
from functools import cached_property
from typing import (
    Any,
    AsyncGenerator,
    Generator,
    Generic,
    ParamSpec,
    Protocol,
    Self,
    TypeVar,
)

from pydantic_mongo_document import compat
from pydantic_mongo_document.types import AsyncPyMongoCursor, PyMongoCursor

if typing.TYPE_CHECKING:
    import pydantic_mongo_document.document.asyncio  # noqa: F401
    import pydantic_mongo_document.document.sync  # noqa: F401
    from pydantic_mongo_document.document.base import DocumentBase  # noqa: F401


P = ParamSpec("P")
Doc = TypeVar("Doc", bound="DocumentBase[Any, Any, Any, Any, Any, Any]")

AG = AsyncGenerator["pydantic_mongo_document.document.asyncio.Document", None]
G = Generator["pydantic_mongo_document.document.sync.Document", None, None]

C = TypeVar("C", bound="Cursor[Any]")
R = TypeVar("R")


class CursorProtoBase(Protocol):
    def __getattr__(self, item): ...

    def __call__(self, *args, **kwargs): ...


class AsyncCursorProto(CursorProtoBase):
    def __aiter__(self) -> Self: ...

    def __anext__(self):
        pass


class SyncCursorProto(CursorProtoBase):
    def __iter__(self) -> Self: ...

    def __next__(self):
        pass


class Cursor(Generic[Doc]):
    def __init__(
        self,
        model_cls: Doc,
        cursor: PyMongoCursor | AsyncPyMongoCursor,
    ) -> None:
        self.model_cls = model_cls
        self.cursor = cursor
        self.generator = None

    @cached_property
    def is_async(self) -> bool:
        return hasattr(self.cursor, "__aiter__")

    def __aiter__(self) -> Self:
        if not self.is_async:
            raise TypeError("Cursor is not async.")

        self.generator = self.cursor.__aiter__()
        return self

    def __iter__(self) -> Self:
        if self.is_async:
            raise TypeError("Cursor is not sync.")

        self.generator = self.cursor.__iter__()
        return self

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> "Cursor[Doc]":
        return Cursor[self.model_cls](self.model_cls, self.cursor(*args, **kwargs))  # type: ignore[name-defined]

    def __getattr__(self, item: str) -> Self | Any:
        value = getattr(self.cursor, item)

        if callable(value):
            return Cursor[self.model_cls](self.model_cls, value)  # type: ignore[name-defined]

        return value

    async def __anext__(self) -> Doc:
        assert self.generator is not None

        if not self.is_async:
            raise TypeError("Cursor is not async.")

        return self.model_cls.model_validate(await compat.anext(self.generator))

    def __next__(self) -> Doc:
        assert self.generator is not None

        if self.is_async:
            raise TypeError("Cursor is not sync.")

        return self.model_cls.model_validate(next(self.generator))
