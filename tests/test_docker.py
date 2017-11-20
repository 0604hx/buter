import inspect
import json
import unittest

import docker
import os
import json

from config import getConfig


class DockerTestCase(unittest.TestCase):
    def setUp(self):
        config = getConfig()

        if config.DOCKER_HOST is not None:
            os.environ['DOCKER_HOST'] = config.DOCKER_HOST
        if config.DOCKER_CERT_PATH is not None:
            os.environ['DOCKER_CERT_PATH'] = config.DOCKER_CERT_PATH
        if config.DOCKER_TLS_VERIFY is not None:
            os.environ['DOCKER_TLS_VERIFY'] = config.DOCKER_TLS_VERIFY

        # 配置 TLSConfig，详见：http://docker-py.readthedocs.io/en/stable/tls.html#docker.tls.TLSConfig
        # tls_config = docker.tls.TLSConfig(
        #     ca_cert=config.DOCKER_CERT_PATH+"/ca.pem",
        #     client_cert=(config.DOCKER_CERT_PATH+'/cert.pem', config.DOCKER_CERT_PATH+'/key.pem'),
        #     verify=True
        # )
        # self.client = docker.DockerClient(base_url=config.DOCKER_HOST, tls=tls_config)
        self.client = docker.from_env()
        # self.client = docker.APIClient()

    """
    从特定的 tar 文件加载 docker image
    """
    def test_image_load(self):
        f = open("G:/alpine.latest.tar", 'rb+')
        self.client.images.load(f.read())
        f.close()

    def test_images(self):
        images = self.client.images.list()
        print(images)

        #
        # 以下代码是使用 jsonpickle 进行序列化，目前并没用上
        #
        # print(jsonpickle.encode(images, unpicklable=False))
        #
        # print(jsonpickle.encode(
        #     Result.ok("这个是result",Result.error(ServiceException("service 出错了"))),
        #     unpicklable=False
        # ))
        #
        # print(jsonpickle.encode(
        #     Application(name="IRCP",version="1.0.0",id=2),
        #     unpicklable=False,
        #     max_depth=2
        # ))


if __name__ == '__main__':
    unittest.main()
