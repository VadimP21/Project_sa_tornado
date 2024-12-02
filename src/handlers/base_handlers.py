"""
Базовые сущности обработчиков
"""

from tornado.web import MissingArgumentError, RequestHandler


class BaseHandler(RequestHandler):
    """
    Базовый класс для обработки запросов, содержащий общую логику обработки исключений.
    """

    def base_request(self, func, *args, **kwargs):
        try:
            result = func(*args, **kwargs)
            self.set_status(201)
            self.write(result)

        except ValueError as exc:
            self.set_status(400)
            self.write({"ValueError": str(exc)})
        except AttributeError as exc:
            self.set_status(400)
            self.write({"AttributeError": str(exc)})
        except MissingArgumentError as exc:
            self.set_status(400)
            self.write({"MissingArgumentError": str(exc)})
        except TypeError as exc:
            self.set_status(400)
            self.write({"TypeError": str(exc)})
        except Exception as exc:
            self.set_status(500)
            self.write({"Unexpected error": str(exc)})
