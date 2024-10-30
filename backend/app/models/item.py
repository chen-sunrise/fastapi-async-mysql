
from pydantic import BaseModel

from app.utils import PydanticObjectId

from .base import MongoObjectBase


class ItemBase(BaseModel):
    title: str
    description: str
    owner: PydanticObjectId


class Item(MongoObjectBase, ItemBase): ...
