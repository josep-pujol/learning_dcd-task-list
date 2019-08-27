import app
import unittest


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()


    def test_home(self):
        result = self.app.get('/')
        print(result)
        print('end test_home')


if __name__ == '__main__':
    unittest.main()
