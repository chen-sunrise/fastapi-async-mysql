from typing import Optional
from app.models import ItemBase
from app.utils import optional, PydanticObjectId


class IItemCreate(ItemBase): 
    owner: Optional[PydanticObjectId] = None


@optional()
class IIUserUpdate(ItemBase): ...


class IItemDetail(ItemBase): ...
