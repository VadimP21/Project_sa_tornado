"""
Файл подключения
"""

import tornado

from src.routers import routers


def app():
    return tornado.web.Application(routers)


if __name__ == "__main__":
    app = app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
