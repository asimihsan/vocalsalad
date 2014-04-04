from __future__ import print_function

import tornado.ioloop

from vocalsalad.app import get_application
import vocalsalad.settings  # NOQA


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
        tornado.ioloop.IOLoop.instance().close(all_fds=True)
        tornado.ioloop.IOLoop.instance().stop()
        print("after stopping")


def main():
    print("woohoo i'm running!")
    Server(host='0.0.0.0',
           port=20080).start()

if __name__ == "__main__":
    main()
