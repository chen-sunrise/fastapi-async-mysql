from typing import Any, List, Optional, Tuple, Union

from app.utils import PydanticObjectId
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING


class QueryBase(BaseModel):
    offset: Optional[int] = None
    limit: Optional[int] = None
    filters: Optional[dict] = None
    order_by: Optional[Any] = None

    id: Optional[Union[PydanticObjectId, str]] = None
    ids: Optional[List[Union[PydanticObjectId, str]]] = None

    def get_sort(self) -> Optional[List[Tuple[str, int]]]:
        if self.order_by is not None:
            assert isinstance(
                self.order_by, list
            ), "Mongodb accept only List[Tuple[str, ASCENDING | DESCENDING]] type ordering"
            if len(self.order_by) == 0:
                return None
            for item in self.order_by:
                assert (
                    isinstance(item, tuple) and len(item) == 2
                ), "Mongodb accept only List[Tuple[str, ASCENDING | DESCENDING]] type ordering"
                assert isinstance(item[0], str) and item[1] in [
                    DESCENDING,
                    ASCENDING,
                ], "Mongodb accept only List[Tuple[str, ASCENDING | DESCENDING]] type ordering"
            return self.order_by
