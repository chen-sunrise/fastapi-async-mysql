from datetime import datetime, timezone
from typing import Optional

from app.utils import PydanticObjectId
from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class PydanticModelConfig:
    allow_population_by_field_name = True

    @classmethod
    def default_dict(cls, **kwargs) -> dict:
        return {"populate_by_name": True, "alias_generator": to_camel, **kwargs}

    @classmethod
    def default(cls, **kwargs) -> ConfigDict:
        return ConfigDict(**cls.default_dict(**kwargs))


class SchemaBase(BaseModel):
    created: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MongoObjectBase(BaseModel):
    id: Optional[PydanticObjectId] = Field(None, alias=AliasChoices("_id", "id"))
