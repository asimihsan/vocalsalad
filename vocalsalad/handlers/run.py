from .base import BaseHandler


class RunHandler(BaseHandler):
    def get(self):
        self.write("pong\n")
