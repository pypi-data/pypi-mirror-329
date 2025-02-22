from typing import TypeAlias

import pymongo.results

from pydantic_mongo_document.document.base import DocumentBase
from pydantic_mongo_document.types import PyMongoClient, PyMongoCollection, PyMongoDatabase

_SYNC_CLIENTS: dict[str, PyMongoClient] = {}

CountReturnType: TypeAlias = int
DeleteReturnType: TypeAlias = pymongo.results.DeleteResult
CommitReturnType: TypeAlias = pymongo.results.UpdateResult | None


class Document(
    DocumentBase[
        PyMongoClient,
        PyMongoDatabase,
        PyMongoCollection,
        CountReturnType,
        DeleteReturnType,
        CommitReturnType,
    ],
):
    """Sync document model."""
