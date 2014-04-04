from .testcases import LiveServerTestCase


class AppRunTestCase(LiveServerTestCase):
    def test_run_only(self):
        """Start a command, do nothing else."""

        self.post('/api/v1/run', {
            'command': 'echo testing',
        })
