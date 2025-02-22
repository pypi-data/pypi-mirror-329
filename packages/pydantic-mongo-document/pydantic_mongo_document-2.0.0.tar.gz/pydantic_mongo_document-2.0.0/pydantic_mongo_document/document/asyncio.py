from typing import Awaitable, TypeAlias

import pymongo.results

from pydantic_mongo_document.document.base import DocumentBase
from pydantic_mongo_document.types import (
    AsyncPyMongoClient,
    AsyncPyMongoCollection,
    AsyncPyMongoDatabase,
)

_ASYNC_CLIENTS: dict[str, AsyncPyMongoClient] = {}


CountReturnType: TypeAlias = Awaitable[int]
DeleteReturnType: TypeAlias = Awaitable[pymongo.results.DeleteResult]
CommitReturnType: TypeAlias = Awaitable[pymongo.results.UpdateResult | None]


class Document(
    DocumentBase[
        AsyncPyMongoClient,
        AsyncPyMongoDatabase,
        AsyncPyMongoCollection,
        CountReturnType,
        DeleteReturnType,
        CommitReturnType,
    ],
):
    """Async document model."""
