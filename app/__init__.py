from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

# 创建app应用,__name__是python预定义变量，被设置为使用本模块.
app = Flask(__name__)
mail = Mail(app)

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    # 错误日志发邮件
    credentials = None
    if Config.MAIL_USERNAME or Config.MAIL_PASSWORD:
        credentials = (Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
    mail_handler = SMTPHandler((Config.MAIL_SERVER, Config.MAIL_PORT), 'no-reply@' + Config.MAIL_SERVER,
                               Config.ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # 写日志到文件
    file_handler = RotatingFileHandler("tmp/microblot.log", "a", 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("microblog startup")


# 添加配置信息
app.config.from_object(Config)

# 建立数据库关系
db = SQLAlchemy(app)
# 绑定app和数据库，以便进行操作
migrate = Migrate(app,db)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, errors
