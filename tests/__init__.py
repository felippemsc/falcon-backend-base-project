import base64
import json
import logging
import os
import sys
from pathlib import Path

from falcon import testing

from config import BaseConfig

from base_project import create_app
from base_project.database import reset_db_for_testing


BASE_DIR = Path(__file__).parent.parent
LOG = logging.getLogger()


def encode_base_auth_header(basic_auth: str):
    return 'Basic {}'.format(
        base64.b64encode(basic_auth.encode('utf-8')).decode('utf-8'))


class TestLogger(testing.TestCase):
    """
    Main class to deal with logs during tests
    """
    tests_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        format=("\n%(asctime)s [%(levelname)s] "
                "[%(module)s:%(funcName)s:%(lineno)s] "
                "[%(threadName)s-%(thread)d] \n%(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S")

    def set_logging(self):
        """
        Configures the log for testing.

        To cleaner output the level is set to the highest.

        Level could be changed for more details during the tests.

        It is possible to override this function to change the log level for specific tests.
        """
        LOG.level = logging.CRITICAL
        LOG.addHandler(self.tests_handler)

    def setUp(self):
        """Configure what is necessary for the tests."""
        super().setUp()
        self.set_logging()


class BaseTest(TestLogger):
    """
    Main class for unit tests
    """
    dir_ = os.path.dirname(__file__)

    def setUp(self):
        """Configure what is necessary for the tests."""
        reset_db_for_testing(BaseConfig.DATABASE_URI)
        super().setUp()

        self.app = create_app(BaseConfig)

    def populate_table(self, model, filename):
        records = []
        with open(f'{BASE_DIR}/tests/db_fixtures/{filename}') as f:
            for line in f.readlines():
                records.append(json.loads(line))

        for record in records:
            model.validate_and_record(record)
