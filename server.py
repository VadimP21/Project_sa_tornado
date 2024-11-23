"""
Файл подключения
"""

import tornado

from src.routers import routers


def make_app():
    return tornado.web.Application(
        routers
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
