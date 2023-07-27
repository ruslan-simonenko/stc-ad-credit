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
    logger = logging.getLogger('env_config.py')
    logger.setLevel(logging.INFO)

    load_dotenv('.env.local')
    app_env = Environment(os.environ.get('APP_ENV', 'prod'))
    logger.info('Preparing database for %s environment.', app_env.value)

    db_path = f'../instance/{app_env.value}.db'
    config.set_main_option(APP_ENV_CONFIG_KEY, app_env.value)
    config.set_main_option('sqlalchemy.url', config.get_main_option('sqlalchemy.url').format(db_path=db_path))
    return config


def get_app_env() -> Environment:
    env = os.environ.get('APP_ENV', 'prod')
    return Environment(env.lower())
