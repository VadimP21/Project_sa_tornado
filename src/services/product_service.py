"""
Сервис для хранения бизнес-логики, валидации и подготовки данных, и выдачи ее конечному пользователю
"""
from os import stat_result

from pydantic import ValidationError

from db_repository.product_repository import ProductRepository
from schemas.product_schemas import ProductPostDTO, ProductGetDTO
from schemas.proj_schemas import ResultToWriteDTO
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
            product_to_post_dto: ProductPostDTO = ProductPostDTO(**kwargs)
        except ValidationError as exc:
            result: ResultToWriteDTO = ResultToWriteDTO(result=exc.json(), status_code=400)
            return result
        last_version_product_bd = ProductRepository.last_version_product_repository(product_to_post_dto)
        if last_version_product_bd:
            try:
                last_version_product_by_name_dto = product_orm_to_dto(last_version_product_bd)
            except

        if last_version_product_by_name_dto:

