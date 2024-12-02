"""
Модуль, содержащий вспомогательные функции,
которые не являются частью основной логики приложения
"""


def product_orm_to_dto(
    product_orm: "ProductOrm", model_gto: "BaseModel"
) -> "BaseModel":
    """
    Функция преобразования Модели БД в Модель DTO
    :param model_gto: pydantic.BaseModel
    :param product_orm: ProductOrm
    :return: ProductGetDTO
    """
    data = dict()
    dto_fields_names: list = list(model_gto.model_fields.keys())

    print("dto_fields_names", dto_fields_names)
    print("product_orm.__dict__.keys()", product_orm.__dict__.keys())
    for field in product_orm.__dict__.keys():
        if field in dto_fields_names:
            data[field] = product_orm.__dict__[field]
    print(data)
    result = model_gto(**data)
    print(result)
    return result
    # data = {field: getattr(product_orm, field) for field in model_gto.model_fields if hasattr(product_orm, field)}
    # return model_gto(*data)
