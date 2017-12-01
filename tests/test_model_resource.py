import unittest

from buter.server import create_app, db
from buter.models import Resource, Application


class ResourceModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing', {'DOCKER_ABLE':False})
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()

    def test_insert(self):
        entity = Resource(name="app.zip", remark="测试的资源", size=102400)
        db.session.add(entity)
        db.session.commit()
        print(entity)

    def test_insert_from_file(self):
        entity = Resource.fromFile("G:/tidb.zip", Application(id=1))
        print(entity)
        db.session.add(entity)
        db.session.commit()
        print(entity)


if __name__ == '__main__':
    unittest.main()
