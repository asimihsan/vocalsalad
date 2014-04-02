import threading
import tornado.ioloop

from vocalsalad.app import application


class Server(object):
    def __init__(self, host, port, is_running):
        self.host = host
        self.port = port
        self.is_running = is_running

    def start(self):
        application.listen(self.port, self.host)
        tornado.ioloop.IOLoop.instance().start()


def main():
    print("woohoo i'm running!")
    Server(host='0.0.0.0',
           port=20080,
           is_running=threading.Event()).start()

if __name__ == "__main__":
    main()
