import unittest
from app import app, db
from app.models import User, Post
from datetime import datetime, timedelta

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://futhead:futhead@localhost:3306/test?charset=utf8"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        # pass
        db.session.remove()
        db.drop_all()

    # def test_avatar(self):
    #     u = User(username="haha", email="haha@163.com")
    #     avatar = u.avatar(128)
    #     expected = "https://www.gravatar.com/avatar/44ff1a7f65f4c7a7299373de4d3f44a2?d=identicon&s=128"
    #     assert avatar[0:len(expected)] == expected

    # def test_follow(self):
    #     u1 = User(username='john', email='john@example.com')
    #     u2 = User(username='susan', email='susan@example.com')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     assert u1.unfollow(u2) == None
    #     u = u1.follow(u2)
    #     db.session.add(u)
    #     db.session.commit()
    #     assert u1.follow(u2) == None
    #     assert u1.is_following(u2)
    #     assert u1.followed.count() == 1
    #     assert u1.followed.first().username == "susan"
    #     assert u2.followers.count() == 1
    #     assert u2.followers.first().username == "john"
    #     u = u1.unfollow(u2)
    #     assert u != None
    #     db.session.add(u)
    #     db.session.commit()
    #     assert u1.is_following(u2) == False
    #     assert u1.followed.count() == 0
    #     assert u2.followers.count() == 0

    # def test_follow_posts(self):
    #     u1 = User(username='john', email='john@example.com')
    #     u2 = User(username='susan', email='susan@example.com')
    #     u3 = User(username='mary', email='mary@example.com')
    #     u4 = User(username='david', email='david@example.com')
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     # make four posts
    #     utcnow = datetime.utcnow()
    #     p1 = Post(body="post from john", author=u1, timestamp=utcnow + timedelta(seconds=1))
    #     p2 = Post(body="post from susan", author=u2, timestamp=utcnow + timedelta(seconds=2))
    #     p3 = Post(body="post from mary", author=u3, timestamp=utcnow + timedelta(seconds=3))
    #     p4 = Post(body="post from david", author=u4, timestamp=utcnow + timedelta(seconds=4))
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.add(p3)
    #     db.session.add(p4)
    #     db.session.commit()
    #     # setup the followers
    #     u1.follow(u1)  # john follows himself
    #     u1.follow(u2)  # john follows susan
    #     u1.follow(u4)  # john follows david
    #     u2.follow(u2)  # susan follows herself
    #     u2.follow(u3)  # susan follows mary
    #     u3.follow(u3)  # mary follows herself
    #     u3.follow(u4)  # mary follows david
    #     u4.follow(u4)  # david follows himself
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     db.session.commit()
    #     # check the followed posts of each user
    #     f1 = u1.followed_posts().all()
    #     f2 = u2.followed_posts().all()
    #     f3 = u3.followed_posts().all()
    #     f4 = u4.followed_posts().all()
    #
    #     assert len(f1) == 3
    #     assert len(f2) == 2
    #     assert len(f3) == 2
    #     assert len(f4) == 1
    #     assert f1 == [p4, p2, p1]
    #     assert f2 == [p3, p2]
    #     assert f3 == [p4, p3]
    #     assert f4 == [p4]

    def test_send_mail(self):
        from flask_mail import Message
        from app import app, mail
        from config import Config

        msg = Message("test subject", sender=Config.ADMINS[0], recipients=Config.ADMINS)
        msg.body = "text body"
        msg.html = "<b>HTML</b>body"
        with app.app_context():
            mail.send(msg)

if __name__ == '__main__':
    unittest.main()