"""
Маршрутизаторы проекта
"""

from tornado.web import URLSpec
from handlers.product_handlers import ProductHandlers, ProductListHandler

routers = [
    URLSpec(r"/product/", ProductHandlers),
    URLSpec(r"/products/", ProductListHandler),
]
