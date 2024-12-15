"""
Маршрутизаторы проекта
"""

from tornado.web import URLSpec, url
from handlers.product_handlers import *

routers = [
    URLSpec(r"/product/", ProductHandlers),
]
