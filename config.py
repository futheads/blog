class Config(object):
    #设置密匙要没有规律，别被人轻易猜到哦
    SECRET_KEY = 'futhead123456'
    # 格式为mysql+pymysql://数据库用户名:密码@数据库地址:端口号/数据库的名字?数据库格式
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://futhead:futhead@localhost:3306/flaskblog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = "localhost"
    MAIL_PORT = 25
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # administrator list
    ADMINS = ["futhead@163.com"]