import tornado.web

from .handlers.ping import PingHandler
from .handlers.run import RunHandler

application = tornado.web.Application([
    (r"/ping", PingHandler),
    (r"/api/v1/run", RunHandler),
])
