from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductPostDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: int


class ProductResultDTO(ProductPostDTO):
    id: int
    version: int


class ProductWithNewVersionPostDTO(ProductPostDTO):
    version: int

class ProductSearchByIdDTO(BaseModel):
    id: int

class ProductSearchByNameDTO(BaseModel):
    name: str


class ProductGetDTO(ProductPostDTO):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    archived: bool | None
