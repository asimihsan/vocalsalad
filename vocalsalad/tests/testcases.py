import threading
import unittest

import vocalsalad.server


class LiveServerThread(threading.Thread):
    """Thread for running the HTTP server while the tests are running.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.is_running = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        server = vocalsalad.server.Server(self.host, self.port, self.is_running)
        server.start()


class LiveServerTestCase(unittest.TestCase):
    """Base TestCase to inherit from which will run an HTTP server in
    a background thread.
    """
    def setUp(self):
        self.server_thread = LiveServerThread(host='127.0.0.1', port=10088)
        self.server_thread.daemon = True
        self.server_thread.start()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        self.server_thread.is_running.clear()
        unittest.TestCase.tearDown(self)
