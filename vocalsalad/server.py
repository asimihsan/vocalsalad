from __future__ import print_function

import tornado.ioloop

from vocalsalad.app import application


class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        application.listen(self.port, self.host)
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        tornado.ioloop.IOLoop.instance().close(all_fds=True)
        tornado.ioloop.IOLoop.instance().stop()
        print("after stopping")


def main():
    print("woohoo i'm running!")
    Server(host='0.0.0.0', port=20080).start()

if __name__ == "__main__":
    main()
