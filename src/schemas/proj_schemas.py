from datetime import datetime

from pydantic import BaseModel


class ResultToWriteDTO(BaseModel):
    result: str
    status_code: int


class ErrorDTO(BaseModel):
    error: str
    status_code: int
