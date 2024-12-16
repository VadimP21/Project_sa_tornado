from pydantic import ValidationError

from db_repository.product_repository import ProductRepository
from models.models import ProductOrm
from schemas.product_schemas import ProductResultDTO, ProductToUpdateDTO
from schemas.proj_schemas import ResponseDTO


def get_product_by_one_field(
    insert_dto_model, repository_func, status_code: int = 201, **kwargs
):
    """ """
    try:
        product_searching_dto = insert_dto_model(**kwargs)
    except ValidationError as exc:
        result: dict = ResponseDTO[str](data=exc.json(), status_code=400).model_dump()
        return result
    searching_product_orm: "ProductOrm" = repository_func(product_searching_dto)
    if not searching_product_orm:
        result: dict = ResponseDTO[str](
            data=f"Product with {product_searching_dto} not found.", status_code=400
        ).model_dump()
        return result

    result_product_dto: "ProductResultDTO" = ProductResultDTO.model_validate(
        searching_product_orm
    )
    result: dict = ResponseDTO[ProductResultDTO](
        data=result_product_dto, status_code=status_code
    ).model_dump()
    return result


def update_product_by_one_field(
    insert_dto_model, repository_find_func, status_code: int = 200, **kwargs
):
    """ """
    ### провалидировать kwargs через две модели ДТО: name+price, name
    try:
        product_searching_dto = insert_dto_model(
            **kwargs
        )  ### ProductUpdateByNameInsertDTO, ProductUpdateByIdInsertDTO
        print(product_searching_dto)
    except ValidationError as exc:
        result: dict = ResponseDTO[str](data=exc.json(), status_code=400).model_dump()
        return result

    searching_product_orm: "ProductOrm" = repository_find_func(
        product_searching_dto  ## last_version_product_by_name_repository, last_version_product_by_id_repository
    )
    if not searching_product_orm:
        result: dict = ResponseDTO[str](
            data=f"Product with {product_searching_dto} not found.", status_code=400
        ).model_dump()
        return result

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
