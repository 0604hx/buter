import unittest

from app.server import create_app,db
from app.models import Application


class ApplicationModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # db.create_all()

    @unittest.skip
    def test_insert(self):
        app = Application(name="tonglian-server", remark="通联服务端")
        db.session.add(app)
        db.session.commit()

    def test_list(self):
        query = Application.query.first()
        print(query)


if __name__ == '__main__':
    unittest.main()
