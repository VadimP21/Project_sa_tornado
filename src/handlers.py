"""
Обработчики
"""

from tornado.web import RequestHandler, MissingArgumentError
from src.queries.orm import SyncORM


class BaseHandler(RequestHandler):
    """
    Базовый класс для обработки запросов, содержащий общую логику обработки исключений.
    """

    def base_request(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            self.set_status(201)
            self.write(result)

        except ValueError as exc:
            self.set_status(400)
            self.write({"ValueError": str(exc)})
        except AttributeError as exc:
            self.set_status(400)
            self.write({"AttributeError": str(exc)})
        except MissingArgumentError as exc:
            self.set_status(400)
            self.write({"MissingArgumentError": str(exc)})
        except Exception as exc:
            self.set_status(500)
            self.write({"Unexpected error": str(exc)})


class MainHandler(RequestHandler):
    """
    Обработчик для получения списка всех элементов каталога и продуктов

    """

    def get(self):
        pass


class GetProductListHandler(RequestHandler):
    """
    Обработчик для получения списка всех продуктов
    """

    def get(self):
        pass


class CreateProductHandler(BaseHandler):
    """
    Обработчик для создания продуктов
    """

    def post(self) -> None:
        name = self.get_argument("name")
        price = self.get_argument("price")
        self.base_request(SyncORM.create_product, name=name, price=price)


class GetProductHandler(RequestHandler):
    """
    Обработчик для получения списка продуктов по названию
    """

    def get(self):
        pass


class UpdateProductHandler(BaseHandler):
    """
    Обработчик для изменения продуктов
    """

    def post(self) -> None:
        product_id = self.get_argument("id")
        new_name = self.get_argument("new_name")
        self.base_request(
            SyncORM.upgrade_product, product_id=product_id, new_name=new_name
        )


class DeleteProductHandler(BaseHandler):
    """
    Обработчик для удаления продуктов
    """

    def post(self) -> None:
        name = self.get_argument("name")
        self.base_request(SyncORM.archive_product, name=name)


class GetCategoryListHandler(RequestHandler):
    """
    Обработчик для получения списка всех элементов каталога
    """

    def get(self):
        pass


class CreateCategoryHandler(BaseHandler):
    """
    Обработчик для создания элементов каталога
    """

    def post(self) -> None:
        name = self.get_argument("name")
        description = self.get_argument("description", default=None)
        self.base_request(SyncORM.create_category, name=name, description=description)


class GetCategoryHandler(RequestHandler):
    """
    Обработчик для получения списка элементов каталога по названию
    """

    def get(self):
        pass


class UpdateCategoryHandler(BaseHandler):
    """
    Обработчик для изменения элементов каталога
    """

    def post(self) -> None:
        category_id = self.get_argument(name="id", default=None)
        new_name = self.get_argument(name="new_name", default=None)
        new_description = self.get_argument(name="new_description", default=None)
        self.base_request(
            SyncORM.update_category,
            category_id=category_id,
            new_name=new_name,
            new_description=new_description,
        )


class DeleteCategoryHandler(BaseHandler):
    """
    Обработчик для удаления элементов каталога
    """

    def post(self) -> None:
        pass
