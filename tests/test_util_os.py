import unittest
from app.util.OSUtil import *


class TestOSUtil(unittest.TestCase):

    def test_getOSInfo(self):
        print("system info : ", getOSInfo())

    def test_getPythonInfo(self):
        print("python info : ", getPythonInfo())

    def test_getDockerInfo(self):
        print("docker info : ", getDockerInfo())


if __name__ == '__main__':
    import os
    os.getenv()
    unittest.main()
