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
            (r"/product/list", GetProductListHandler),
            (r"/product/([^/]+)", GetProductHandler),
            (r"/product/", CreateProductHandler),
            (r"/product/update/([^/]+)", UpdateProductHandler),
            (r"/category/list", GetCategoryListHandler),
            (r"/category/([^/]+)", GetCategoryHandler),
            (r"/category/", CreateCategoryHandler),
            (r"/category/update/([^/]+)", UpdateCategoryHandler),
            (r"/category/delete/([^/]+)", DeleteCategoryHandler),
        ]
    )


if __name__ == "__main__":
    # Base.metadata.create_all(bind=engine)
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
