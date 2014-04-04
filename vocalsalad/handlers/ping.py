from .base import BaseHandler


class PingHandler(BaseHandler):
    def get(self):
        self.write("pong\n")
