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
    archived: bool | None


class ProductSearchByIdDTO(BaseModel):
    """
    DTO for Get query
    """

    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductSearchByNameDTO(BaseModel):
    """
    DTO for Get query
    """

    name: str


class ProductUpdateByNameInsertDTO(BaseModel):
    """
    DTO Patch query
    """

    model_config = ConfigDict(from_attributes=True)
    name: str
    price: int


class ProductUpdateByIdInsertDTO(BaseModel):
    """
    DTO Patch query
    """

    model_config = ConfigDict(from_attributes=True)
    id: int
    price: int


class ProductToUpdateDTO(ProductSearchByIdDTO):
    """
    DTO Patch query
    """

    model_config = ConfigDict(from_attributes=True)


class ProductArchivedByIdInsertDTO(BaseModel):
    """
    DTO Delete query
    """

    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductArchivedByNameInsertDTO(BaseModel):
    """
    DTO Patch query
    """

    model_config = ConfigDict(from_attributes=True)
    name: str


class ProductToArchiveDTO(ProductSearchByNameDTO):
    """
    DTO Patch query
    """

    model_config = ConfigDict(from_attributes=True)


class ProductGetDTO(ProductPostDTO):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime
    archived: bool | None
