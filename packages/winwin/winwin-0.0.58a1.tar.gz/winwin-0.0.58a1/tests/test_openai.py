import unittest

import winwin

class MyTestCase(unittest.TestCase):
    def test_something(self):
        res = winwin.support.openai_api()
        print(res)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
