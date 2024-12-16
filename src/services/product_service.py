"""
Сервис для хранения бизнес-логики, валидации и подготовки данных, и выдачи ее конечному пользователю
"""

from pydantic import ValidationError

from db_repository.product_repository import ProductRepository
from models.models import ProductOrm
from schemas.product_schemas import (
    ProductPostDTO,
    ProductResultDTO,
    ProductWithNewVersionPostDTO,
    ProductSearchByIdDTO,
    ProductSearchByNameDTO, ProductUpdateByNameInsertDTO,
)
from schemas.proj_schemas import ResponseDTO
from utils.service import get_product_by_one_field, update_product_by_one_field


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
            result: dict = ResponseDTO[str](
                data=exc.json(), status_code=400
            ).model_dump()
            return result

        last_version_product_orm: str | None = (
            ProductRepository.last_version_product_by_name_repository(
                product_to_post_dto
            )
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
        result: dict = ResponseDTO[ProductResultDTO](
            data=new_product_dto, status_code=201
        ).model_dump()
        return result

    @staticmethod
    def read_one(**kwargs) -> dict[str, str]:
        """
        Метод для получения продукта по имени(последняя версия) или ID
        args: kwarg = {"name": ..., "price": ...}
        return: {data: {created product}, status_code: 200 | 400}
        """

        if kwargs["id"] and kwargs["name"]:
            exp_msg = "Insert only ID or only 'name'"
            result: dict = ResponseDTO[str](data=exp_msg, status_code=400).model_dump()
            return result

        elif kwargs["id"]:
            return get_product_by_one_field(
                insert_dto_model=ProductSearchByIdDTO,
                repository_func=ProductRepository.last_version_product_by_id_repository,
                status_code=201,
                **kwargs
            )

        elif kwargs["name"]:
            return get_product_by_one_field(
                insert_dto_model=ProductSearchByNameDTO,
                repository_func=ProductRepository.last_version_product_by_name_repository,
                status_code=201,
                **kwargs
            )

        else:
            exp_msg = "Insert ID or 'name'"
            result: dict = ResponseDTO[str](data=exp_msg, status_code=400).model_dump()
            return result

    @staticmethod
    def update(**kwargs) -> dict[str, str]:
        """
        Метод изменяет поля существующего продукта
        args: kwarg = {"name": ..., "price": ...}
        return: {data: {created product}, status_code: 200 | 400}
        """
        if kwargs["id"] and kwargs["name"]:
            exp_msg = "Insert only ID or only 'name' for product updating"
            result: dict = ResponseDTO[str](data=exp_msg, status_code=400).model_dump()
            return result

        elif not kwargs["price"]:
            exp_msg = "Insert new price for product updating"
            result: dict = ResponseDTO[str](data=exp_msg, status_code=400).model_dump()
            return result

        elif kwargs["name"] and kwargs["price"]:
            update_product_by_one_field(
                insert_dto_model=ProductUpdateByNameInsertDTO,
                repository_func=ProductRepository.last_version_product_by_name_repository,
                **kwargs
            )
        elif kwargs["id"] and kwargs["price"]:
            pass
