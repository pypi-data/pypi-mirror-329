import datetime
import json
import typing
from enum import Enum
from functools import cached_property
from typing import Any

import bson  # type: ignore[import-untyped]
import pydantic
from pydantic import BaseModel, SecretStr
from pydantic_core import Url

if typing.TYPE_CHECKING:
    from pydantic_mongo_document import ObjectId


class JsonEncoder(json.JSONEncoder):
    CONTEXT = {"document": True}

    @cached_property
    def object_id_type(self) -> pydantic.TypeAdapter["ObjectId"]:
        from pydantic_mongo_document import ObjectId

        return pydantic.TypeAdapter(ObjectId)

    def is_object_id_string(self, o: Any) -> bool:
        try:
            return self.object_id_type.validate_python(o) is not None
        except ValueError:
            return False

    def encode(self, o: Any, reveal_secrets: bool = False) -> Any:
        if isinstance(o, Enum):
            return o.value

        if isinstance(o, BaseModel):
            return o.model_dump_json(context=self.CONTEXT)

        if isinstance(o, (set, list, tuple)):
            return [self.encode(item) for item in o]

        if isinstance(o, dict):
            return self.encode_dict(o, reveal_secrets=reveal_secrets)

        if isinstance(o, SecretStr) and reveal_secrets:
            return o.get_secret_value()

        if isinstance(o, (bson.ObjectId, SecretStr, Url)):
            return str(o)

        if isinstance(o, (int, float, bool)):
            return o

        if isinstance(o, (datetime.datetime, datetime.timedelta)):
            return o

        if isinstance(o, str) and self.is_object_id_string(o):
            return bson.ObjectId(o)

        if isinstance(o, str):
            return o

        if o is None:
            return None

        return super().encode(o)

    def encode_dict(self, obj: dict[str, Any], reveal_secrets: bool = False) -> dict[str, Any]:
        """Encodes all values in dict."""

        encoded = {}
        for key, value in obj.items():
            if isinstance(value, dict):
                encoded[key] = self.encode_dict(value, reveal_secrets=reveal_secrets)
            else:
                encoded[key] = self.encode(value, reveal_secrets=reveal_secrets)

        return encoded
