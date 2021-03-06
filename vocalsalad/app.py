import tornado.web

from .handlers.ping import PingHandler
from .handlers.run import RunHandler


def get_application(**settings):
    return tornado.web.Application([
        (r"/ping", PingHandler),
        (r"/api/v1/run", RunHandler),
    ], **settings)
