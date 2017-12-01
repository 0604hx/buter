import json
import unittest

from buter.app.services import load_from_file, detect_app_name
from buter.server import docker
from buter.util.Utils import unzip
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

    def test_json_read(self):
        with open("G:/app.json") as content:
            app = json.load(content)  # '{"name":"abc"}'

        print(app)
        docker.createContainer("pingcap/tidb", app['cmd'], app['args'])

    def test_detect_app_name(self):
        app = json.loads('{"image":"pingcap/tidb", "args":{"name":"tidb01"}}')
        self.assertEqual("tidb", detect_app_name(None, app['image']))
        self.assertEqual("tidb01", detect_app_name(app['args']))
        self.assertEqual("tidb", detect_app_name("tidb"))

    def test_unzip(self):
        file_path = "G:/test/test.zip"
        unzip(file_path, "G:/test")


if __name__ == '__main__':
    unittest.main()
