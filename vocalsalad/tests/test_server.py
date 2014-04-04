import multiprocessing
import os
import requests
import signal
import subprocess
import time
import unittest


SERVER_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, "server.py"))


def server_process():
    """We want to get the test coverage up so we wrap this command
    in 'coverage', which is already a test dependency of this module.
    This instruments the command to output coverage stats.
    """
    global process
    process = None

    def handler(signum, frame):
        process.send_signal(signal.SIGTERM)
        process.wait()
    signal.signal(signal.SIGTERM, handler)
    process = subprocess.Popen("coverage run --parallel-mode %s" % SERVER_PATH, shell=True)
    process.wait()
    print("server_process child process ended")


class ServerTestCase(unittest.TestCase):
    """Just that vocalsalad/server.py can be run and launches the
    server. Doesn't do anything else.
    """

    @classmethod
    def setUpClass(cls):
        cls.server_process = multiprocessing.Process(
            target=server_process)
        cls.server_process.daemon = True
        cls.server_process.start()

        # The first time the tornado server comes up after already
        # being up sometimes we get a TCP connection error. Let's catch
        # that and wait for the server to come up.
        start = time.time()
        while True:
            try:
                requests.get(cls.get_server_url() + "/ping")
            except requests.ConnectionError:
                time.sleep(0.1)
                if time.time() - start > 1:
                    raise
            else:
                break

    @classmethod
    def tearDownClass(cls):
        print("killing server")
        cls.server_process.terminate()
        cls.server_process.join()

    @classmethod
    def get_server_url(cls):
        return "http://127.0.0.1:20080"

    def test_server_starts(self):
        uri = self.get_server_url() + "/ping"
        request = requests.get(uri)
        self.assertEqual(request.text, "pong\n")
