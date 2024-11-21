"""
Маршрутизатор проекта
"""

import tornado

from database import Base, engine
from handlers import *


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/product", CreateProductHandler),
            (r"/product-list", GetProductListHandler),
            (r"/product/update", UpdateProductHandler),
            (
                r"/product/delete",
                DeleteProductHandler,
            ),
            (r"/product/([^/]+)", GetProductHandler),
            (r"/category", CreateCategoryHandler),
            (r"/category-list", GetCategoryListHandler),
            (r"/category/update", UpdateCategoryHandler),
            (r"/category/delete", DeleteCategoryHandler),
            (r"/category/([^/]+)", GetCategoryHandler),
        ]
    )


if __name__ == "__main__":
    # Base.metadata.create_all(bind=engine)
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
