from typing import Annotated, Any, Literal, TypeVar

import bson  # type: ignore[import-untyped]
import bson.json_util  # type: ignore[import-untyped]
import pymongo.asynchronous.collection
import pymongo.asynchronous.cursor
import pymongo.asynchronous.database
import pymongo.asynchronous.mongo_client
import pymongo.collection
import pymongo.database
from pydantic import BeforeValidator, StringConstraints

T = TypeVar("T")

_ObjectIdString = Annotated[
    str, StringConstraints(min_length=24, max_length=24, pattern=r"^[a-f\d]{24}$")
]

_DictObjectId = dict[Literal["$oid"], _ObjectIdString]


def check_object_id(value: _ObjectIdString | _DictObjectId) -> str:
    if isinstance(value, dict):
        value = value["$oid"]

    if not bson.ObjectId.is_valid(value):
        raise ValueError("Invalid ObjectId")

    return str(value)


ObjectId = Annotated[
    _ObjectIdString,
    BeforeValidator(check_object_id),
]


PyMongoDocType = dict[str, Any]

PyMongoCursor = pymongo.cursor.Cursor[PyMongoDocType]
AsyncPyMongoCursor = pymongo.asynchronous.cursor.AsyncCursor[PyMongoDocType]

PyMongoClient = pymongo.MongoClient[PyMongoDocType]
AsyncPyMongoClient = pymongo.asynchronous.mongo_client.AsyncMongoClient[PyMongoDocType]

PyMongoDatabase = pymongo.database.Database[PyMongoDocType]
AsyncPyMongoDatabase = pymongo.asynchronous.database.AsyncDatabase[PyMongoDocType]

PyMongoCollection = pymongo.collection.Collection[PyMongoDocType]
AsyncPyMongoCollection = pymongo.asynchronous.collection.AsyncCollection[PyMongoDocType]

__all__ = [
    "ObjectId",
    "PyMongoDocType",
    "AsyncPyMongoCursor",
    "PyMongoCursor",
    "PyMongoClient",
    "AsyncPyMongoClient",
    "PyMongoDatabase",
    "AsyncPyMongoDatabase",
    "PyMongoCollection",
    "AsyncPyMongoCollection",
]
