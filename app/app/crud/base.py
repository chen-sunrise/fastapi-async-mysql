from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()
    
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return [o for o in result.scalars().all()]

    def pre_commit_create(self, *, obj_in: Union[CreateSchemaType, Dict[str, Any]]) -> ModelType:
        _obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**_obj_in_data)
        return db_obj
    
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        obj = self.pre_commit_create(obj_in=obj_in)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    
    def pre_commit_update(
            self, *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj = self.pre_commit_update(db_obj=db_obj, obj_in=obj_in)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def remove(self, db: AsyncSession, *, id: int) -> ModelType:
        obj = db.get(self.model, id)
        await db.delete(obj)
        await db.commit()
        return obj