import os

# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENV = "development"
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="BAD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASEDIR, 'instance', 'stage.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PRODUCTION_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'production.db')}",
    )


class StageConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI",
        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}",
    )
    WTF_CSRF_ENABLED = False
