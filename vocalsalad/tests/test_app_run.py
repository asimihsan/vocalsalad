from .testcases import LiveServerTestCase


class AppRunTestCase(LiveServerTestCase):
    def _start_run_echo_testing(self):
        return self.post('/api/v1/run/start', {
            'command': 'echo testing',
        })

    def _get_run_stdout(self, ident):
        return self.get('/api/v1/run/%s/get_stdout' % ident)

    def test_run_only(self):
        """Start a command, do nothing else."""

        self._start_run_echo_testing()

    def test_run_returns_id(self):
        """Start a command, check there's a command_id in JSON response.
        """
        data = self._start_run_echo_testing().json()
        self.assertIn("id", data)

    def test_run_then_get_stdout(self):
        """Start a command, get its stdout.
        """
        data = self._start_run_echo_testing().json()
        stdout = self._get_run_stdout(data["id"])
        self.assertEqual("testing\n", stdout)
