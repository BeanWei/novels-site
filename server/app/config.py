APP_ENV = "testing"

class BaseConfig:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "naeb"
    WEB_ADMIN = '157318439@qq.com'
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    FLASK_MAIL_SENDER = ""
    FLASK_MAIL_SUBJECT_PREFIX = "[知了]"

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Bean:124127@localhost:3306/novels"

class DevelopmentConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Bean:124127@localhost:3306/novels"

config = {
    "testing": TestingConfig,
    "devolopment": DevelopmentConfig
}