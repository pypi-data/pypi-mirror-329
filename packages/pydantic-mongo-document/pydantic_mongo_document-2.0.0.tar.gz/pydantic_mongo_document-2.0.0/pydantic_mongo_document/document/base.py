import asyncio
from abc import ABC, abstractmethod
from functools import cached_property
from typing import (
    Any,
    Awaitable,
    ClassVar,
    Generic,
    List,
    Optional,
    Self,
    Type,
    TypeVar,
    Union,
    cast,
)

import bson
import pymongo.errors
import pymongo.results
from pydantic import BaseModel, ConfigDict, Field, validate_call
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.results import InsertOneResult
from pymongo.synchronous.client_session import ClientSession

from pydantic_mongo_document import ObjectId
from pydantic_mongo_document.config import ReplicaConfig
from pydantic_mongo_document.cursor import Cursor
from pydantic_mongo_document.encoder import JsonEncoder
from pydantic_mongo_document.exceptions import DocumentNotFound
from pydantic_mongo_document.misc import async_wrap, get_model_generic_value
from pydantic_mongo_document.types import (
    AsyncPyMongoClient,
    AsyncPyMongoCollection,
    AsyncPyMongoDatabase,
    PyMongoClient,
    PyMongoCollection,
    PyMongoDatabase,
)

CONFIG: dict[str, ReplicaConfig] = {}
"""Map of replicas to mongo URIs."""

# Type variables
Doc = TypeVar("Doc", bound="DocumentBase[Any, Any, Any, Any, Any, Any]")

ClientType = TypeVar("ClientType", bound=Union[PyMongoClient, AsyncPyMongoClient])
DatabaseType = TypeVar("DatabaseType", bound=Union[PyMongoDatabase, AsyncPyMongoDatabase])
CollectionType = TypeVar("CollectionType", bound=Union[PyMongoCollection, AsyncPyMongoCollection])
SessionType = TypeVar("SessionType", bound=Union[ClientSession, AsyncClientSession])

CountReturnType = TypeVar("CountReturnType", bound=Union[int, Awaitable[int]])
DeleteReturnType = TypeVar(
    "DeleteReturnType",
    bound=pymongo.results.DeleteResult | Awaitable[pymongo.results.DeleteResult],
)
CommitReturnType = TypeVar(
    "CommitReturnType",
    bound=Optional[pymongo.results.UpdateResult]
    | Awaitable[Optional[pymongo.results.UpdateResult]],
)

_CLIENTS: dict[
    Union[type[PyMongoClient], type[AsyncPyMongoClient]],
    dict[str, Union[PyMongoClient, AsyncPyMongoClient]],
] = {}


class DocumentBase(
    BaseModel,
    Generic[
        ClientType,
        DatabaseType,
        CollectionType,
        CountReturnType,
        DeleteReturnType,
        CommitReturnType,
    ],
):
    model_config = ConfigDict(populate_by_name=True)

    __primary_key__: ClassVar[str] = "id"

    __replica__: ClassVar[str]
    """Mongodb replica name."""

    __database__: ClassVar[str]
    """Mongodb database name."""

    __collection__: ClassVar[str]
    """Mongodb collection name."""

    __clients__: ClassVar[dict[str, Any]] = {}
    """Map of clients for each database."""

    __document__: dict[str, Any]
    """Document data. For internal use only."""

    NotFoundError: ClassVar[Type[Exception]] = DocumentNotFound
    DuplicateKeyError: ClassVar[Type[Exception]] = pymongo.errors.DuplicateKeyError

    encoder: ClassVar[JsonEncoder] = JsonEncoder()

    id: ObjectId = Field(default_factory=lambda: str(bson.ObjectId()), alias="_id")

    def model_post_init(self, __context: Any) -> None:
        self.__document__ = self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def client(cls) -> ClientType:
        """Returns client for database."""

        client_cls = get_model_generic_value(cls, ClientType)
        clients = _CLIENTS.setdefault(client_cls, {})

        if cls.__replica__ not in clients:
            clients[cls.__replica__] = client_cls(
                host=str(cls.get_replica_config().uri),
                **cls.get_replica_config().client_options.model_dump(
                    mode="json",
                    by_alias=True,
                    exclude_none=True,
                ),
            )

        return clients[cls.__replica__]

    @classmethod
    def database(cls) -> DatabaseType:
        return cast(DatabaseType, cls.client()[cls.__database__])

    @classmethod
    def collection(cls) -> CollectionType:
        """Returns collection for document."""

        return cast(CollectionType, cls.database()[cls.__collection__])

    @property
    def primary_key(self) -> Any:
        return getattr(self, self.__primary_key__)

    @classmethod
    def get_replica_config(cls) -> ReplicaConfig:
        return CONFIG[cls.__replica__]

    @property
    def primary_key_field_name(self) -> str:
        return self.model_fields[self.__primary_key__].alias or self.__primary_key__

    @cached_property
    def is_async(self) -> bool:
        return asyncio.iscoroutinefunction(self.collection().find_one)

    @classmethod
    @validate_call
    def set_replica_config(cls, config: dict[str, ReplicaConfig]) -> None:
        CONFIG.clear()
        CONFIG.update(config)

    @classmethod
    def create_indexes(cls) -> Awaitable[None] | None:
        """Creates indexes for collection."""

        return async_wrap(asyncio.sleep(0) if cls.is_async else None, lambda _: None)

    @classmethod
    def _inner_one(
        cls,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        session: Optional[SessionType] = None,
        **kwargs: Any,
    ) -> Optional[dict[str, Any]] | Awaitable[dict[str, Any]]:
        """Finds one document by ID."""

        query = {}
        if document_id is not None:
            query["_id"] = document_id
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        return cast(
            Optional[dict[str, Any]] | Awaitable[dict[str, Any]],
            cls.collection().find_one(query, **kwargs, session=session),
        )

    @classmethod
    def one(
        cls,
        /,
        document_id: str | None = None,
        add_query: dict[str, Any] | None = None,
        required: bool = True,
        session: Optional[SessionType] = None,
        **kwargs: Any,
    ) -> Optional[Self | Awaitable[Optional[Self]]]:
        """Finds one document by ID."""

        def _validate(res: Optional[dict[str, Any]]) -> Optional[Self]:
            if res is not None:
                return cls.model_validate(res)

            if required:
                raise cls.NotFoundError()

            return None

        result = cls._inner_one(document_id, add_query, session=session, **kwargs)

        return async_wrap(result, _validate)

    @classmethod
    def all(
        cls,
        document_ids: List[str | bson.ObjectId] | None = None,
        add_query: dict[str, Any] | None = None,
        session: Optional[SessionType] = None,
        **kwargs: Any,
    ) -> Cursor[Self]:  # noqa
        """Finds all documents based in IDs."""

        query = {}
        if document_ids is not None:
            query["_id"] = {"$in": document_ids}
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        cursor_cls = Cursor[cls]  # type: ignore[valid-type]

        return cursor_cls(cls, cls.collection().find(query, **kwargs, session=session))

    @classmethod
    def count(
        cls,
        add_query: dict[str, Any] | None = None,
        session: Optional[SessionType] = None,
        **kwargs: Any,
    ) -> CountReturnType:
        """Counts documents in collection."""

        query = {}
        if add_query is not None:
            query.update(add_query)

        query = cls.encoder.encode_dict(query, reveal_secrets=True)

        return cast(
            CountReturnType,
            cls.collection().count_documents(query, **kwargs, session=session),
        )

    def delete(
        self,
        session: Optional[SessionType] = None,
    ) -> DeleteReturnType:
        """Deletes document from collection."""

        query = self.encoder.encode_dict(
            {self.primary_key_field_name: self.primary_key},
        )

        return cast(DeleteReturnType, self.collection().delete_one(query, session=session))

    def commit_changes(
        self,
        fields: Optional[List[str]] = None,
        session: Optional[SessionType] = None,
    ) -> CommitReturnType:
        """Saves changes to document.

        :param fields: Fields of the document to update in database.
        :param session: Session for transaction.
        """

        search_query: dict[str, Any] = self.encoder.encode_dict(
            {self.primary_key_field_name: self.primary_key}
        )
        update_query: dict[str, Any] = {}

        if not fields:
            fields = [field for field in self.model_fields.keys() if field != self.__primary_key__]

        data = self.encoder.encode_dict(
            self.model_dump(by_alias=True, exclude_none=True),
            reveal_secrets=True,
        )

        for field in fields:
            if field in data and data[field] != self.__document__.get(field):
                update_query.setdefault("$set", {}).update({field: data[field]})
            elif field not in data and field in self.__document__:
                update_query.setdefault("$unset", {}).update({field: ""})

        if update_query:
            return cast(
                CommitReturnType,
                self.collection().update_one(
                    search_query,
                    update_query,
                    session=session,
                ),
            )

        return cast(CommitReturnType, self.noop())

    def insert(
        self,
        session: Optional[SessionType] = None,
    ) -> Self | Awaitable[Self]:
        """Inserts document into collection."""

        def _set_pk(insert_result: InsertOneResult) -> Self:
            if getattr(self, self.__primary_key__, None) is None:
                setattr(self, self.__primary_key__, insert_result.inserted_id)

            return self

        result = self.collection().insert_one(
            self.encoder.encode_dict(
                self.model_dump(by_alias=True, exclude_none=True),
                reveal_secrets=True,
            ),
            session=session,
        )

        return async_wrap(result, _set_pk)

    def noop(self) -> Awaitable[None] | None:
        """No operation. Does nothing."""

        return async_wrap(asyncio.sleep(0) if self.is_async else None, lambda _: None)

    @classmethod
    def find_one(cls, *args, **kwargs):
        """Proxy method for collection.find_one."""

        return cls.collection().find_one(*args, **kwargs)

    @classmethod
    def find(cls, *args, **kwargs):
        """Proxy method for collection.find."""

        return cls.collection().find(*args, **kwargs)

    @classmethod
    def find_one_and_update(cls, *args, **kwargs):
        """Proxy method for collection.find_one_and_update."""

        return cls.collection().find_one_and_update(*args, **kwargs)

    @classmethod
    def find_one_and_replace(cls, *args, **kwargs):
        """Proxy method for collection.find_one_and_replace."""

        return cls.collection().find_one_and_replace(*args, **kwargs)

    @classmethod
    def find_one_and_delete(cls, *args, **kwargs):
        """Proxy method for collection.find_one_and_delete."""

        return cls.collection().find_one_and_delete(*args, **kwargs)

    @classmethod
    def aggregate(cls, *args, **kwargs):
        """Proxy method for collection.aggregate."""

        return cls.collection().aggregate(*args, **kwargs)
