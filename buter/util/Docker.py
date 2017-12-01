import docker
import os


class DockerApi:
    """
    对 docker client 进行封装
    """

    client = None

    def __init__(self, config=None):
        if config is not None:
            self.setup(config)

    def setup(self, config):
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

    def version(self):
        """
        获取docker版本信息，返回结果示例：
        {
            'Arch': 'amd64',
            'Version': '17.09.0-ce',
            'MinAPIVersion': '1.12',
            'GitCommit': 'afdb6d4',
            'BuildTime': '2017-09-26T22:40:56.000000000+00:00',
            'KernelVersion': '4.10.0-40-generic',
            'ApiVersion': '1.32',
            'Os': 'linux',
            'GoVersion': 'go1.8.3'
        }
        :return:
        """
        return self.client.version()

    def loadImage(self, tar_file: str):
        """
        把目标 tar 文件加载为 docker 镜像，类似于 docker image load 命令
        :param tar_file:
        :return:
        """
        file = open(tar_file, 'rb+')
        self.client.images.load(file.read())
        file.close()

    def createContainer(self, image, command=None, args={}):
        """
        参考 dockerClient.create() 方法
        :param args:
        :param image:
        :param command:
        :return:
        """
        return self.client.containers.create(image, command, **args)

    def removeContainerByName(self, name: str):
        return self.client.containers.prune({name: name})

    def removeContainerById(self, cid):
        return self.client.containers.prune({id: cid})

    def getContainer(self, id_or_name):
        return self.client.containers.get(id_or_name)


def init_docker(config):
    return DockerApi(config)
