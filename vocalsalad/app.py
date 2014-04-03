import tornado.web

from .handlers.ping import PingHandler

application = tornado.web.Application([
    (r"/ping", PingHandler),
])
