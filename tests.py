import unittest
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://futhead:futhead@localhost:3306/test?charset=utf8"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username="haha", email="haha@163.com")
        avatar = u.avatar(128)
        expected = "https://www.gravatar.com/avatar/44ff1a7f65f4c7a7299373de4d3f44a2?d=identicon&s=128"
        assert avatar[0:len(expected)] == expected

if __name__ == '__main__':
    unittest.main()