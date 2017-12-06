import inspect
import unittest

import time

import sys

from buter.schedule import jobs
from buter.server import create_app


def test(depth=0):
    frame = sys._getframe(depth)
    code = frame.f_code

    print("frame depth = ", depth)
    print("func name = ", code.co_name)
    print("func filename = ", code.co_filename)
    print("func lineno = ", code.co_firstlineno)
    print("func locals = ", frame.f_locals)


def b():
    print("B.b()")
    stack = inspect.stack()
    the_class = stack[1][0].f_locals["self"].__class__
    the_method = stack[1][0].f_code.co_name
    print("  I was called by {}.{}()".format(str(the_class), the_method))


class JobsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing', {
            'DOCKER_HOST': "tcp://192.168.99.100:2376",
            'DOCKER_CERT_PATH': "C:\\Users\\Administrator\\.docker\\machine\\certs",
            'DOCKER_TLS_VERIFY': "1"
        })
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()

    def test_check_docker(self):
        time.sleep(1)
        print("开始检测 docker。。。")
        jobs.checkDocker()


if __name__ == '__main__':
    unittest.main()
