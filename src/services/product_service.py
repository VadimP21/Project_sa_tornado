"""
Сервис для хранения бизнес-логики, валидации и подготовки данных, и выдачи ее конечному пользователю
"""

from pydantic import ValidationError

from db_repository.product_repository import ProductRepository
from models.models import ProductOrm
from schemas.product_schemas import (
    ProductPostDTO,
    ProductWithNewVersionPostDTO,
    ProductResultDTO,
)
from schemas.proj_schemas import ResultToWriteDTO, ErrorDTO
from utils.base import product_orm_to_dto


class ProductService:
    """
    Класс-сервис для работы с Product.
    Принимает ключевые аргументы из Handler, валидирует, приводит к модели DTO.
    Передает в репозиторий и принимает обратно модель БД, валидирует, приводит к модели DTO.
    """

    @staticmethod
    def post(**kwargs):
        try:
            product_to_post_dto: "ProductPostDTO" = ProductPostDTO(**kwargs)
        except ValidationError as exc:
            result: "ErrorDTO" = ErrorDTO(error=exc.json(), status_code=400)
            return result
        last_version_of_product: int | None = (
            ProductRepository.last_version_of_product_repository(product_to_post_dto)
        )
        if last_version_of_product:
            kwargs["version"] = last_version_of_product + 1
            product_to_post_dto: ProductWithNewVersionPostDTO = (
                ProductWithNewVersionPostDTO(**kwargs)
            )
            new_product_orm: "ProductOrm" | None = (
                ProductRepository.create_new_version_of_existing_product(
                    product_to_post_dto
                )
            )
            new_product_dto: "ProductResultDTO" = product_orm_to_dto(
                product_orm=new_product_orm, model_gto=ProductResultDTO
            )
            result: str = new_product_dto.json()
            if result:
                return ResultToWriteDTO(result=result, status_code=201)
        else:
            #  условие, если создаваемого продукта нет
            #  создать новый продукт v.1
            pass
