from pydantic import ValidationError

from db_repository.product_repository import ProductRepository
from models.models import ProductOrm
from schemas.product_schemas import ProductResultDTO, ProductToUpdateDTO
from schemas.proj_schemas import ResponseDTO


def get_product_by_one_field(
    insert_dto_model, repository_find_func, status_code: int = 201, **kwargs
):
    """
    Фунция получает существующий продукт
    Args:
        insert_dto_model: модель DTO для валидации входных данных
        repository_find_func: функия репозиторий для поиска продукта в БД по идентификатору
        status_code: успешный статус код, по-дефолту 201
        **kwargs: входные данные идентификации
    return:
        result_validation_error: dict, ResponseDTO[str] Ошибка валидации в соответствии insert_dto_model
        result_not_found_error: dict, ResponseDTO[str] Ошибка валидации возвращенной из БД ORM модели
        result: dict, ResponseDTO[ProductResultDTO] успешный ответ
    """
    try:
        product_searching_dto = insert_dto_model(**kwargs)
    except ValidationError as exc:
        result_validation_error: dict = ResponseDTO[str](
            data=exc.json(), status_code=400
        ).model_dump()
        return result_validation_error
    searching_product_orm: "ProductOrm" = repository_find_func(product_searching_dto)
    if not searching_product_orm:
        result_not_found_error: dict = ResponseDTO[str](
            data=f"Product with {product_searching_dto} not found.", status_code=400
        ).model_dump()
        return result_not_found_error

    result_product_dto: "ProductResultDTO" = ProductResultDTO.model_validate(
        searching_product_orm
    )
    result: dict = ResponseDTO[ProductResultDTO](
        data=result_product_dto, status_code=status_code
    ).model_dump()
    return result


def update_product_by_one_field(
    insert_dto_model, repository_find_func, status_code: int = 201, **kwargs
):
    """
    Фунция изменяет существующий продукт
    Args:
        insert_dto_model: модель DTO для валидации входных данных
        repository_find_func: функия репозиторий для поиска продукта в БД по идентификатору
        status_code: успешный статус код, по-дефолту 201
        **kwargs: входные данные идентификации
    return:
        result_validation_error: dict, ResponseDTO[str] Ошибка валидации в соответствии insert_dto_model
        result_not_found_error: dict, ResponseDTO[str] Ошибка валидации возвращенной из БД ORM модели
        result: dict, ResponseDTO[ProductResultDTO] успешный ответ
    """
    try:
        product_searching_dto = insert_dto_model(**kwargs)
        print(product_searching_dto)
    except ValidationError as exc:
        result_validation_error: dict = ResponseDTO[str](
            data=exc.json(), status_code=400
        ).model_dump()
        return result_validation_error

    searching_product_orm: "ProductOrm" = repository_find_func(product_searching_dto)
    if not searching_product_orm:
        result_not_found_error: dict = ResponseDTO[str](
            data=f"Product with {product_searching_dto} not found.", status_code=400
        ).model_dump()
        return result_not_found_error
    product_to_update_dto: "ProductToUpdateDTO" = ProductToUpdateDTO.model_validate(
        searching_product_orm
    )  ### DTO id

    updated_product_orm: "ProductOrm" = (
        ProductRepository.update_last_version_of_existing_product_by_id_repository(
            product_to_update_dto=product_to_update_dto,  # id
            product_with_new_price_dto=product_searching_dto,  # name, price
        )
    )

    result: dict = ResponseDTO[ProductResultDTO](
        data=updated_product_orm, status_code=status_code
    ).model_dump()
    return result
