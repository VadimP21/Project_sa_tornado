"""
Маршрутизаторы проекта
"""

from tornado.web import URLSpec, url
from handlers.product_handlers import *

routers = [
    URLSpec(r"/product/", ProductHandlers),
    URLSpec(r"/product", ProductHandlers),
    # url(r"/product/update", ProductHandlers),
    # (r"/product", CreateProductHandler),
    # (r"/product-list", GetProductListHandler),
    # (r"/product/update", UpdateProductHandler),
    # (
    #     r"/product/delete",
    #     DeleteProductHandler,
    # ),
    # (r"/product/([^/]+)", GetProductHandler),
    # (r"/category", CreateCategoryHandler),
    # (r"/category-list", GetCategoryListHandler),
    # (r"/category/update", UpdateCategoryHandler),
    # (r"/category/delete", DeleteCategoryHandler),
    # (r"/category/([^/]+)", GetCategoryHandler),
]
