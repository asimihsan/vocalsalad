import testcases


class AppTestCase(testcases.LiveServerTestCase):
    def first_test(self):
        self.assertTrue(True)
