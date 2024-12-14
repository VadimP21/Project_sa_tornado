"""
Файл подключения
"""

import tornado

from src.routers import routers, routers_v_2, routers_v_3


def app():
    return tornado.web.Application(routers)


if __name__ == "__main__":
    app = app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
