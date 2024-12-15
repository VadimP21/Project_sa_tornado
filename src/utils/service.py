from pydantic import ValidationError

from schemas.product_schemas import ProductResultDTO
from schemas.proj_schemas import ResponseDTO


def get_product_by_one_field(insert_dto_model, repository_func, status_code: int = 200, **kwargs):
    """ """
    try:
        product_searching_dto = insert_dto_model(**kwargs)
    except ValidationError as exc:
        result: dict = ResponseDTO[str](
            data=exc.json(), status_code=400
        ).model_dump()
        return result
    last_version_of_searching_product_orm: "ProductOrm" = repository_func(
        product_searching_dto
    )
    if not last_version_of_searching_product_orm:
        result: dict = ResponseDTO[str](
            data=f"Product with {product_searching_dto} not found.", status_code=400
        ).model_dump()
        return result

    read_one_product_dto: "ProductResultDTO" = ProductResultDTO.model_validate(
        last_version_of_searching_product_orm
    )
    result: dict = ResponseDTO[ProductResultDTO](
        data=read_one_product_dto, status_code=status_code
    ).model_dump()
    return result
