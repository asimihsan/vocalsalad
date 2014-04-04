#!/usr/bin/env python

from __future__ import print_function

import signal

import tornado.ioloop

from vocalsalad.app import get_application


def handler(signum=None, frame=None):
    try:
        tornado.ioloop.IOLoop.instance().close(all_fds=True)
    except ValueError:
        pass
    try:
        tornado.ioloop.IOLoop.instance().stop()
    except ValueError:
        pass
signal.signal(signal.SIGTERM, handler)


class Server(object):
    def __init__(self, host, port, **application_settings):
        self.host = host
        self.port = port
        self.application_settings = application_settings

    def start(self):
        application = get_application(**self.application_settings)
        application.listen(self.port, self.host)
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        handler()


def main():
    print("woohoo i'm running!")
    Server(host='0.0.0.0',
           port=20080).start()

if __name__ == "__main__":
    main()
