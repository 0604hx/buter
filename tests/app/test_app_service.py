import unittest
from buter.app.services import load_from_file
from buter.server import docker
from config import getConfig


class AppServiceTest(unittest.TestCase):

    def setUp(self):
        """
        这里只需要初始化 server.docker 对象
        :return:
        """
        config = getConfig('dev')

        docker.setup(config)

    def test_load_from_file(self):
        load_from_file("G:/tidb.zip")

    def test_load_image(self):
        docker.loadImage("G:/tidb.tar")


if __name__ == '__main__':
    unittest.main()
