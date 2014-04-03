import tornado.web


class RunHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("pong\n")
