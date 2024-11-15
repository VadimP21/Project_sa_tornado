"""
Хендлеры
"""

from tornado.web import RequestHandler


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
        pass


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
        pass


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
        pass


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
