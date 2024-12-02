"""
Модуль, содержащий вспомогательные функции,
которые не являются частью основной логики приложения
"""

from models.models import ProductOrm
from schemas.product_schemas import ProductGetDTO


def product_orm_to_dto(product_orm: ProductOrm) -> ProductGetDTO:
    """
    Функция преобразования Модели БД в Модель DTO
    :param product_orm: ProductOrm
    :return: ProductGetDTO
    """
    data = dict()
    dto_fields_names: list = list(ProductGetDTO.model_fields.keys())
    for field in product_orm.__dict__.keys():
        if field in dto_fields_names:
            data[field] = product_orm.__dict__[field]
    return ProductGetDTO(**data)
