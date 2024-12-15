from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductPostDTO(BaseModel):
    """
    DTO Post query
    """
    model_config = ConfigDict(from_attributes=True)
    name: str
    price: int


class ProductWithNewVersionPostDTO(ProductPostDTO):
    """
    DTO for Post query
    """
    version: int


class ProductResultDTO(ProductPostDTO):
    """
    DTO Result for CRUD
    """
    id: int
    version: int


class ProductSearchByIdDTO(BaseModel):
    """
    DTO for Get query
    """
    id: int


class ProductSearchByNameDTO(BaseModel):
    """
    DTO for Get query
    """
    name: str


class ProductUpdateInsertDTO(BaseModel):
    """
    DTO Patch query
    """
    model_config = ConfigDict(from_attributes=True)
    name: str


class ProductGetDTO(ProductPostDTO):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    archived: bool | None
