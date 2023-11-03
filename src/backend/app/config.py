from os import environ, path
import bcrypt

from dotenv import load_dotenv

basedir = path.abspath(path.join(path.dirname(__file__), '..'))
# loading env vars from .env file
load_dotenv()

#加载环境变量
#根据不同环境要求自定义应用程序的行为

class BaseConfig(object):
    ''' Base config class. '''

    APP_NAME = environ.get('APP_NAME') or 'upskill-backend'
    ORIGINS = ['*']
    EMAIL_CHARSET = 'UTF-8'
    API_KEY = environ.get('API_KEY')
    # BROKER_URL = environ.get('BROKER_URL')
    # RESULT_BACKEND = environ.get('RESULT_BACKEND')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get(
        'SQLALCHEMY_DATABASE_URI')

    # Authentication
    JWT_SECRETKEY = environ.get('BCRYPT_HASH')
    # bcrypt.hashpw(bytes(environ.get('BCRYPT_HASH'), 'UTF-8'), bcrypt.gensalt())

    LOG_INFO_FILE = path.join(basedir, 'log', 'info.log')
    # LOG_CELERY_FILE = path.join(basedir, 'log', 'celery.log')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] - %(name)s - %(levelname)s - '
                '%(message)s',
                'datefmt': '%b %d %Y %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'log_info_file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_INFO_FILE,
                'maxBytes': 16777216,  # 16megabytes
                'formatter': 'standard',
                'backupCount': 5
            },
        },
        'loggers': {
            APP_NAME: {
                'level': 'DEBUG',
                'handlers': ['log_info_file'],
            },
        },
    }

    # CELERY_LOGGING = {
    #     'format': '[%(asctime)s] - %(name)s - %(levelname)s - '
    #     '%(message)s',
    #     'datefmt': '%b %d %Y %H:%M:%S',
    #     'filename': LOG_CELERY_FILE,
    #     'maxBytes': 10000000,  # 10megabytes
    #     'backupCount': 5
    # }


class Development(BaseConfig):
    ''' Development config. '''

    DEBUG = True
    ENV = 'dev'


class Staging(BaseConfig):
    ''' Staging config. '''

    DEBUG = True
    ENV = 'staging'


class Production(BaseConfig):
    ''' Production config '''

    ENV = 'production'


config = {
    'development': Development,
    'staging': Staging,
    'production': Production,
}
