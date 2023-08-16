import logging
import os
from enum import Enum

from alembic.config import Config
from dotenv import load_dotenv

APP_ENV_CONFIG_KEY = 'stc.app_env'


class Environment(Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'


def update_config_from_env(config: Config) -> Config:
    logger = logging.getLogger('db_migration.env_config')

    app_env = Environment(os.environ.get('APP_ENV', 'prod'))
    load_dotenv(f'env.{app_env}')
    load_dotenv(f'env.local')
    logger.info('Preparing database for %s environment.', app_env.value)
    if app_env == Environment.PROD:
        user = os.environ['DB_USER']
        password = os.environ['DB_PASSWORD']
        host = os.environ['DB_HOST']
        name = os.environ['DB_NAME']
        db_path = f'mysql+mysqlconnector://{user}:{password}@{host}/{name}'
    else:
        db_path = f'sqlite:///../instance/{app_env.value}.db'
    config.set_main_option(APP_ENV_CONFIG_KEY, app_env.value)
    config.set_main_option('sqlalchemy.url', config.get_main_option('sqlalchemy.url').format(db_path=db_path))
    return config


def get_app_env() -> Environment:
    env = os.environ.get('APP_ENV', 'prod')
    return Environment(env.lower())
