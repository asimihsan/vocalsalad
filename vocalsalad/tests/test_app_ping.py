from nose.tools import eq_

from .testcases import LiveServerTestCase


class AppPingTestCase(LiveServerTestCase):
    """Just test that /ping works. This is a sanity test to make sure
    that the Tornado web server can run at all, and indeed that our
    test infrastructure is able to run it etc.

    Run the test more than once because initially there were errors
    to do with repeated requests.
    """
    def _do_ping(self):
        eq_("pong\n", self.get("/ping").text)

    def test_ping(self):
        """Just send a ping, expect pong. #1.
        """
        self._do_ping()

    def test_ping_2(self):
        """Just send a ping, expect pong. #2.
        """
        self._do_ping()

    def test_ping_3(self):
        """Just send a ping, expect pong. #3.
        """
        self._do_ping()
