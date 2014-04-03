import tornado.web


class PingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("pong\n")

application = tornado.web.Application([
    (r"/ping", PingHandler),
])
