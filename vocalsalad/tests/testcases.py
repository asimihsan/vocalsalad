import json
import logging
import multiprocessing
import socket
import sys
import threading
import time
import unittest

import requests

import vocalsalad.log
import vocalsalad.settings
import vocalsalad.server


def find_free_ports(how_many=1):
    """Return a list of n free port numbers on localhost"""
    results = []
    sockets = []
    for x in range(how_many):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        # work out what the actual port number it's bound to is
        addr, port = s.getsockname()
        results.append(port)
        sockets.append(s)

    for s in sockets:
        s.close()

    return results


def live_server_process(host, port, log_queue, **application_settings):
    vocalsalad.log.disable_existing_logging()
    vocalsalad.log.worker_configurer(log_queue)
    server = vocalsalad.server.Server(
        host, port, **application_settings)
    try:
        server.start()
    finally:
        sys.stdout.close()
        server.stop()


class LiveServerTestCase(unittest.TestCase):
    """Base TestCase to inherit from which will run an HTTP server in
    a background thread.
    """

    @classmethod
    def _start_log_listener(cls):
        cls.log_queue = multiprocessing.Queue(-1)
        cls.log_listener = threading.Thread(
            target=vocalsalad.log.listener_thread,
            args=(cls.log_queue, vocalsalad.log.null_configurer))
        cls.log_listener.start()

    @classmethod
    def setUpClass(cls):
        vocalsalad.log.disable_existing_logging()
        cls._start_log_listener()
        cls.logger = logging.getLogger("vocalsalad.test.LiveServerTestCase")
        cls.host = '127.0.0.1'
        cls.port = find_free_ports(1)[0]
        cls.server_process = multiprocessing.Process(
            target=live_server_process, args=(cls.host, cls.port, cls.log_queue),
            kwargs={"debug": True})
        cls.server_process.daemon = True
        cls.server_process.start()

        # The first time the tornado server comes up after already
        # being up sometimes we get a TCP connection error. Let's catch
        # that and wait for the server to come up.
        start = time.time()
        while True:
            try:
                cls.get('/ping')
            except requests.ConnectionError:
                time.sleep(0.1)
                if time.time() - start > 1:
                    raise
            else:
                break

    @classmethod
    def tearDownClass(cls):
        cls.server_process.terminate()
        cls.server_process.join()
        cls.log_queue.put(None)
        cls.log_listener.join()

    @classmethod
    def get_live_server_url(cls):
        return 'http://%s:%s' % (cls.host, cls.port)

    @classmethod
    def get(cls, path, params=None):
        uri = cls.get_live_server_url() + path
        if params is None:
            params = {}
        request = requests.get(uri, params=params)
        request.raise_for_status()
        return request

    @classmethod
    def post(cls, path, data=None):
        uri = cls.get_live_server_url() + path
        if data is None:
            data = {}
        request = requests.get(uri, data=json.dumps(data))
        request.raise_for_status()
        return request
