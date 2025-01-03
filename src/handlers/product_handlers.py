"""
Обработчики запросов по сущности 'Продукт'
"""

from tornado.web import RequestHandler

from handlers.base_handlers import BaseHandler
from services.product_service import ProductService
from src.db_repository.product_repository import SyncORM


class ProductHandlers(RequestHandler):
    """
    Класс-обработчик CRUD для сущности Продукт
    """

    def get(self):
        """
        Функция получения последней версии продукта по ID или имени
        """
        product_id = self.get_query_argument("product_id", None)
        name = self.get_query_argument("name", None)
        kwargs = {
            "name": name,
            "id": product_id,
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
        print("delete")
        kwargs = {
            "id": self.get_argument("product_id", None),
            "name": self.get_argument("name", None),
        }
        result = ProductService.archive(**kwargs)
        self.set_status(status_code=int(result["status_code"]))
        self.write(chunk=result["data"])


class GetProductListHandler(BaseHandler):
    """
    Обработчик для получения списка всех продуктов
    """

    def get(self):
        page_number = self.get_argument("page_number", "1")
        page_size = self.get_argument("page_size", "20")
        sort_field = self.get_argument("sort_field", "id")
        sort_order = self.get_argument("sort_order", "asc")
        product_version = self.get_argument("product_version", "last")
        self.base_request(
            SyncORM.get_product_list,
            page_number=page_number,
            page_size=page_size,
            sort_field=sort_field,
            sort_order=sort_order,
            product_version=product_version,
        )


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
