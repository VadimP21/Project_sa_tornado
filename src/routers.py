"""
Маршрутизаторы проекта
"""

from tornado.web import URLSpec
from handlers.product_handlers import *

routers = [
    URLSpec(r"/product", ProductHandlers, name="product_post"),
    URLSpec(r"/product/update", ProductHandlers, name="product_update"),
    # (r"/product", CreateProductHandler),
    (r"/product-list", GetProductListHandler),
    # (r"/product/update", UpdateProductHandler),
    (
        r"/product/delete",
        DeleteProductHandler,
    ),
    (r"/product/([^/]+)", GetProductHandler),
    # (r"/category", CreateCategoryHandler),
    # (r"/category-list", GetCategoryListHandler),
    # (r"/category/update", UpdateCategoryHandler),
    # (r"/category/delete", DeleteCategoryHandler),
    # (r"/category/([^/]+)", GetCategoryHandler),
]

routers_v_2 = [
    URLSpec(r"/product", ProductHandlers, name="product_post"),  # POST /product
    URLSpec(
        r"/product-list", ProductHandlers, name="product_list_get"
    ),  # GET /product-list
    URLSpec(
        r"/product/update", ProductHandlers, name="product_update_put"
    ),  # PUT /product/update
    URLSpec(
        r"/product/delete", ProductHandlers, name="product_delete_delete"
    ),  # DELETE /product/delete
    URLSpec(
        r"/product/([^/]+)", ProductHandlers, name="product_get_by_id"
    ),  # GET /product/123
]
