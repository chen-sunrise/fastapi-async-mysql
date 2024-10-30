from typing import Annotated, Any
from uuid import UUID

from bson import Binary
from pydantic_core import core_schema


class UUIDAnnotation:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        uuid_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ]
        )
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([core_schema.is_instance_schema(UUID), uuid_schema]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: x if isinstance(x, UUID) else UUID(x)
            ),
        )

    @classmethod
    def validate(cls, value):
        if isinstance(value, Binary):
            return UUID(bytes=value)
        elif isinstance(value, str):
            return UUID(value)
        elif isinstance(value, UUID):
            return value
        raise ValueError("Invalid UUID value")


PydanticUuid = Annotated[UUID, UUIDAnnotation]
