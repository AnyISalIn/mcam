import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    TERRAFORM_BIN = os.environ.get('MCAM_TERRAFORM_BIN') or '/usr/local/bin/terraform'
    PLAN_DIR = os.environ.get('MCAM_PLAN_DIR') or '/plans'
    RQ_REDIS_URL = os.environ.get('MCAM_REDIS_URL') or 'redis://localhost:6379/0'
    MONGODB_SETTINGS = {
        'host': os.getenv('MCAM_MONGO_URI', 'mongodb://mcam:mcam@db:27017/mcam'),
        'connect': False
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class StageConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'stage': StageConfig,
    'default': DevelopmentConfig,
}
