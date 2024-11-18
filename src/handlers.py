"""
Хендлеры
"""

from tornado.web import RequestHandler
from src.queries.orm import SyncORM


class MainHandler(RequestHandler):
    """
    Хендлер для получения списка всех элементов каталога и продуктов

    """

    def get(self):
        pass


class GetProductListHandler(RequestHandler):
    """
    Хендлер для получения списка всех продуктов
    """

    def get(self):
        pass


class CreateProductHandler(RequestHandler):
    """
    Хендлер для создания продуктов
    """

    def post(self) -> None:
        name = self.get_argument("name")
        price = self.get_argument("price")
        try:
            result = SyncORM.create_product(name=name, price=int(price))
            self.set_status(201)
            self.write(result)
        except Exception as exc:
            self.set_status(500)
            self.write({"error": str(exc)})


class GetProductHandler(RequestHandler):
    """
    Хендлер для получения списка продуктов по названию
    """

    def get(self):
        pass


class UpdateProductHandler(RequestHandler):
    """
    Хендлер для изменения продуктов
    """

    def post(self) -> None:
        pass


class DeleteProductHandler(RequestHandler):
    """
    Хендлер для удаления продуктов
    """

    def post(self) -> None:
        name = self.get_argument("name")
        try:
            result = SyncORM.archive_product(name=name)
            self.set_status(201)
            self.write(result)
        except Exception as exc:
            self.set_status(500)
            self.write({"error": str(exc)})


class GetCategoryListHandler(RequestHandler):
    """
    Хендлер для получения списка всех элементов каталога
    """

    def get(self):
        pass


class CreateCategoryHandler(RequestHandler):
    """
    Хендлер для создания элементов каталога
    """

    def post(self) -> None:
        name = self.get_argument("name")
        description = self.get_argument("description")
        try:
            result = SyncORM.create_category(name=name, description=description)
            self.set_status(201)
            self.write(result)
        except Exception as exc:
            self.set_status(500)
            self.write({"error": str(exc)})


class GetCategoryHandler(RequestHandler):
    """
    Хендлер для получения списка элементов каталога по названию
    """

    def get(self):
        pass


class UpdateCategoryHandler(RequestHandler):
    """
    Хендлер для изменения элементов каталога
    """

    def post(self) -> None:
        pass


class DeleteCategoryHandler(RequestHandler):
    """
    Хендлер для удаления элементов каталога
    """

    def post(self) -> None:
        pass
