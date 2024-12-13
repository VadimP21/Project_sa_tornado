"""
Сервис для хранения бизнес-логики, валидации и подготовки данных, и выдачи ее конечному пользователю
"""

from pydantic import ValidationError

from db_repository.product_repository import ProductRepository
from models.models import ProductOrm
from schemas.product_schemas import (
    ProductPostDTO,
    ProductWithNewVersionPostDTO,
    ProductResultDTO, ProductSearchByIdDTO, ProductSearchByNameDTO,
)
from schemas.proj_schemas import ErrorDTO, ResponseDTO


class ProductService:
    """
    Класс-сервис для работы с Product.
    Принимает ключевые аргументы из Handler, валидирует, приводит к модели DTO.
    Передает в репозиторий и принимает обратно модель БД, валидирует, приводит к модели DTO.
    """

    @staticmethod
    def create(**kwargs) -> dict[str, str]:
        """
        Метод создает новый продукт,
        если продукт существует, добавляет его новую версию
        args: kwarg = {"name": ..., "price": ...}
        return: {data: {created product}, status_code: 201 | 400}
        """
        try:
            product_to_post_dto: "ProductPostDTO" = ProductPostDTO(**kwargs)
        except ValidationError as exc:
            result: dict = ResponseDTO[str](data=exc.json(), status_code=400).model_dump()
            return result

        last_version_product_orm: "ProductOrm" = (
            ProductRepository.last_version_product_by_name_repository(product_to_post_dto)
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
        else:
            new_product_orm: "ProductOrm" = ProductRepository.create_product(
                product_to_post_dto
            )
            new_product_dto: "ProductResultDTO" = ProductResultDTO.model_validate(
                new_product_orm
            )
        result: dict = ResponseDTO[ProductResultDTO](data=new_product_dto, status_code=201).model_dump()
        return result



        result: dict = ResponseDTO[ProductResultDTO](data=new_product_dto, status_code=201).model_dump()
        return result

            result: str = new_product_dto.model_dump_json()
            return ResultToWriteDTO(result=result, status_code=201)

    @staticmethod
    def update(**kwargs):
        """ """
        pass
