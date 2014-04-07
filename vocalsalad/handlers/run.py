import logging

from tornado.escape import json_decode
from tornado.web import HTTPError

from .base import BaseHandler


class RunStartHandler(BaseHandler):
    log = logging.getLogger("vocalsalad.handlers.run.RunStartHandler")

    def post(self):
        try:
            data = json_decode(self.request.body)
        except ValueError:
            raise HTTPError(400, "Expected valid JSON.")
        self.log.info("data: %s" % data)
        self.write({"id": "1"})


class RunHandler(BaseHandler):
    log = logging.getLogger("vocalsalad.handlers.run.RunHandler")
    operations = set(["get_stdout"])

    def get(self, identifier, operation):
        if operation not in self.operations:
            raise HTTPError(400, "Unsupported operation: %s" % operation)
        getattr(self, operation)(identifier)

    def get_stdout(self, identifier):
        self.write("testing\n")
