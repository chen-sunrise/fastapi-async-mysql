from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult

from app import models, schemas
from app.core import settings
from app.core.security import get_password_hash, verify_password
from app.utils import QueryBase

from .base import CRUDBase


class CRUDUser(CRUDBase[models.User, schemas.IUserCreate, schemas.IUserUpdate]):
    async def get_by_username(self, db: AsyncIOMotorClient, *, username: str) -> Optional[models.User]:
        return await self.first(db, query=QueryBase(filters={"username": username}))

    async def get_by_email(self, db: AsyncIOMotorClient, *, email: str) -> Optional[models.User]:
        return await self.first(db, query=QueryBase(filters={"email": email}))

    async def authenticate(self, db: AsyncIOMotorClient, *, email: str, password: str) -> Optional[models.User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def create(self, db: AsyncIOMotorClient, *, obj_in: schemas.IUserCreate) -> InsertOneResult:
        user_in = models.User(
            email=obj_in.email, hashed_password=get_password_hash(obj_in.password), username=obj_in.username
        )
        return await super().create(db, obj_in=user_in)


user = CRUDUser(models.User, database=settings.MONGO_DB_DATABASE, collection=settings.MONGO_DB_USER_COLLECTION)
