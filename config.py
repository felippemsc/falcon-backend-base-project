import logging.config
import os

from pathlib import Path

LOG = logging.getLogger()

BASE_DIR = Path(__file__).parent


class BaseConfig:
    API_VERSION = os.getenv('API_VERSION')

    LOG.info(f'Config Falcon Base Project. Version:{API_VERSION}')

    DB_NAME = os.getenv('DB_ENDPOINT', 'my_db_name')  # TODO
    DB_SCHEMA = os.getenv('DB_SCHEMA', 'my_db_schema')  # TODO
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DATABASE_URI = os.getenv('DATABASE_URI', f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
