from typing import Annotated, Literal, Optional

from pydantic import BaseModel, Field


class ClientOptions(BaseModel):
    read_preference: Optional[
        Literal[
            "PRIMARY",
            "PRIMARY_PREFERRED",
            "SECONDARY",
            "SECONDARY_PREFERRED",
            "NEAREST",
        ]
    ] = Field(None, description="Read preference.")
    write_concern: Optional[Literal["majority", "local"]] = Field(
        None,
        description="Write concern.",
    )
    read_concern: Optional[Literal["majority", "local"]] = Field(
        None,
        description="Read concern.",
    )


class ReplicaConfig(BaseModel):
    """Mongodb replica config model."""

    uri: Annotated[
        str,
        Field(..., description="Mongodb connection URI."),
    ]
    client_options: ClientOptions = Field(
        default_factory=ClientOptions,
        description="Mongodb client options.",
    )
