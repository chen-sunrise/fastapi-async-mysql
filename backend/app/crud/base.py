from typing import Generic, List, Optional, TypeVar

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo.results import (
    InsertManyResult,
    InsertOneResult,
)

from app.utils import QueryBase

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType, collection: str, database: str):
        self.model = model
        self.database = database
        self.collection = collection

    async def first_by_id(self, db: AsyncIOMotorClient, *, _id: str) -> Optional[ModelType]:
        doc = await db[self.database][self.collection].find_one({"_id": ObjectId(_id)})
        return self.model(**doc)

    async def get_by_ids(self, db: AsyncIOMotorClient, *, _ids: List[str]) -> List[ModelType]:
        cursor = await db[self.database][self.collection].find({"_id": {"$in": [ObjectId(_id) for _id in _ids]}})
        return list(map(lambda doc: self.model(**doc), cursor.to_list(length=len(_ids))))

    async def first(self, db: AsyncIOMotorClient, *, query: QueryBase) -> Optional[ModelType]:
        doc = await db[self.database][self.collection].find_one(query.filters or {})
        return self.model(**doc) if doc is not None else None

    async def get_multi(self, db: AsyncIOMotorClient, *, query: QueryBase) -> List[ModelType]:
        assert query.offset is not None and query.limit is not None, "offset and limit is require for listing query"
        cursor = db[self.database][self.collection].find(query.filters or {})
        _sort = query.get_sort()
        if _sort is not None and len(_sort) > 0:
            cursor = cursor.sort(_sort)
        docs = await cursor.skip(query.offset).limit(query.limit).to_list(query.limit)
        return list(map(lambda doc: self.model(**doc), docs))

    async def create(self, db: AsyncIOMotorClient, *, obj_in: ModelType) -> InsertOneResult:
        return await db[self.database][self.collection].insert_one(obj_in.model_dump(by_alias=True))

    async def create_multi(self, db: AsyncIOMotorClient, *, obj_in_list: List[ModelType]) -> InsertManyResult:
        _obj_in_list = list(map(lambda obj_in: obj_in.model_dump(by_alias=True), obj_in_list))
        return await db[self.database][self.collection].insert_many(_obj_in_list)

    async def update(self, db: AsyncIOMotorClient, *, _id: str, obj_in: UpdateSchemaType | dict):
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        await db[self.database][self.collection].update_one({"_id": ObjectId(_id)}, {"$set": update_data})

    async def delete(self, db: AsyncIOMotorClient, *, _id: str):
        await db[self.database][self.collection].delete_one({"_id": ObjectId(_id)})
