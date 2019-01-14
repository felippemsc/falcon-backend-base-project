import os
import json
import base64
from pathlib import Path

from falcon import testing, HTTP_OK

from config import BaseConfig

from base_project import create_app
from base_project.database import reset_db_for_testing


BASE_DIR = Path(__file__).parent.parent


def encode_base_auth_header(basic_auth: str):
    return 'Basic {}'.format(
        base64.b64encode(basic_auth.encode('utf-8')).decode('utf-8'))


class BaseTest(testing.TestCase):
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
            result = model.record_from_dict(record)  # TODO: use the validate and record func
