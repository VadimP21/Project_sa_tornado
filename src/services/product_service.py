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


class ProductService:
    """
    Класс-сервис для работы с Product.
    Принимает ключевые аргументы из Handler, валидирует, приводит к модели DTO.
    Передает в репозиторий и принимает обратно модель БД, валидирует, приводит к модели DTO.
    """

    @staticmethod
    def create(**kwargs):
        """
        Метод создает новый продукт,
        если продукт существует, добавляет его новую версию
        """
        try:
            product_to_post_dto: "ProductPostDTO" = ProductPostDTO(**kwargs)
        except ValidationError as exc:
            result: "ErrorDTO" = ErrorDTO(error=exc.json(), status_code=400)
            return result

        last_version_product_orm: "ProductOrm" = (
            ProductRepository.last_version_product_repository(product_to_post_dto)
        )

        if last_version_product_orm:
            kwargs["version"] = last_version_product_orm.version + 1
            product_to_post_dto: ProductWithNewVersionPostDTO = (
                ProductWithNewVersionPostDTO(**kwargs)
            )
            new_product_orm: "ProductOrm" | None = (
                ProductRepository.create_new_version_of_existing_product(
                    product_to_post_dto
                )
            )
            new_product_dto: "ProductResultDTO" = ProductResultDTO.model_validate(
                new_product_orm
            )

            result: str = new_product_dto.model_dump_json()
            return ResultToWriteDTO(result=result, status_code=201)

        else:
            new_product_orm: "ProductOrm" = ProductRepository.create_product(
                product_to_post_dto
            )
            new_product_dto: "ProductResultDTO" = ProductResultDTO.model_validate(
                new_product_orm
            )

            result: str = new_product_dto.model_dump_json()
            return ResultToWriteDTO(result=result, status_code=201)

    @staticmethod
    def update(**kwargs):
        """ """
        pass
