from typing import Annotated

import jwt
from app import crud, models, schemas
from app.core import security, settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/access-token")


def get_async_mongo():
    db = None
    try:
        db = AsyncIOMotorClient(settings.MONGO_DB_URI, UuidRepresentation="standard")
        yield db
    finally:
        db.close()


async def get_current_user(
    db: AsyncIOMotorClient = Depends(get_async_mongo), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.first_by_id(db, _id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


AsyncMongoClient = Annotated[AsyncIOMotorClient, Depends(get_async_mongo)]
CurrentUser = Annotated[models.User, Depends(get_current_user)]
