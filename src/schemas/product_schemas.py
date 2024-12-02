from datetime import datetime

from pydantic import BaseModel


class ProductPostDTO(BaseModel):
    name: str
    price: int


class ProductGetDTO(ProductPostDTO):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    archived: bool | None


