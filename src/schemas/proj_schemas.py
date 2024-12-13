from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

DataT = TypeVar('DataT')

class ResponseDTO(BaseModel, Generic[DataT]):
    data: DataT
    status_code: int


class ErrorDTO(BaseModel):
    error: str
    status_code: int
