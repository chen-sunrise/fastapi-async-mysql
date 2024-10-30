from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.utils import optional
from app.models import UserBase


class IUserCreate(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


@optional()
class IUserUpdate(BaseModel):
    email: EmailStr
    username: str
    # password: str

class IUserDetail(UserBase):
    hashed_password: str = Field(exclude=True)