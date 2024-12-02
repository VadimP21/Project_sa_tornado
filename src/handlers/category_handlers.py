"""
Обработчики запросов по сущности 'Категория'
"""

from tornado.web import RequestHandler

from handlers.base_handlers import BaseHandler
from src.db_repository.product_repository import SyncORM


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
        category_id = self.get_argument(name="id", default=None)
        self.base_request(
            SyncORM.archive_category,
            category_id=category_id,
        )
