"""
Обработчики запросов по сущности 'Продукт'
"""

from tornado.web import RequestHandler
from services.product_service import ProductService


class ProductHandlers(RequestHandler):
    """
    Класс-обработчик CRUD для сущности Продукт
    """

    def get(self):
        """
        Функция получения последней версии продукта по ID или имени
        """
        kwargs = {
            "name": self.get_query_argument("product_id", None),
            "id": self.get_query_argument("name", None),
        }
        result = ProductService.read_one(**kwargs)
        self.set_status(status_code=int(result["status_code"]))
        self.write(chunk=result["data"])

    def post(self) -> None:
        """
        Функция создания нового продукта или последней версии нового продукта
        """
        kwargs = {
            "name": self.get_argument("name"),
            "price": self.get_argument("price"),
        }
        result = ProductService.create(**kwargs)
        self.set_status(status_code=int(result["status_code"]))
        self.write(chunk=result["data"])

    def patch(self):
        """
        Функция изменения стоимости продукта по ID или имени
        """
        kwargs = {
            "id": self.get_argument("product_id", None),
            "name": self.get_argument("name", None),
            "price": self.get_argument("price"),
        }
        result = ProductService.update(**kwargs)
        self.set_status(status_code=int(result["status_code"]))
        self.write(chunk=result["data"])

    def delete(self):
        """
        Функция софт-удаления продукта по ID или имени
        """
        kwargs = {
            "id": self.get_argument("product_id", None),
            "name": self.get_argument("name", None),
        }
        result = ProductService.archive(**kwargs)
        self.set_status(status_code=int(result["status_code"]))
        self.write(chunk=result["data"])


class ProductListHandler(RequestHandler):
    """
    Обработчик для получения списка всех продуктов
    """

    def get(self):
        """
        Функция получения списка продуктов
        """

        page_number = self.get_argument("page_number", "1")
        page_size = self.get_argument("page_size", "20")
        sort_field = self.get_argument("sort_field", "id")
        sort_order = self.get_argument("sort_order", "asc")
        product_version = self.get_argument("product_version", "last")
        kwargs = {
            "page_number": page_number,
            "page_size": page_size,
            "sort_field": sort_field,
            "sort_order": sort_order,
            "product_version": product_version,
        }
        result = ProductService.read_one(**kwargs)
        self.set_status(status_code=int(result["status_code"]))
        self.write(chunk=result["data"])
