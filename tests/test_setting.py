import unittest

from config import getConfig


class SettingTestCase(unittest.TestCase):

    def test_something(self):
        config = getConfig()

        for k in [kk for kk in dir(config) if not kk.startswith("__")]:
            print(k,"=", getattr(config, k))



if __name__ == '__main__':
    unittest.main()
