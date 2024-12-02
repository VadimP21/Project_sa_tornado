from dataclasses import field
from datetime import datetime

from black.nodes import first_leaf
from pydantic import BaseModel


class ProductPostDTO(BaseModel):
    name: str
    price: int


class ProductResultDTO(ProductPostDTO):
    id: int


class ProductWithNewVersionPostDTO(ProductPostDTO):
    version: int


class ProductGetDTO(ProductPostDTO):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    archived: bool | None
