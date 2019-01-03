import os
import json
from pathlib import Path

from falcon import testing

from config import BaseConfig

from base_project import create_app


BASE_DIR = Path(__file__).parent.parent


class BaseTest(testing.TestCase):
    """
    Main class for unit tests
    """
    dir_ = os.path.dirname(__file__)

    def setUp(self):
        """Configure what is necessary for the tests."""
        super().setUp()

        self.app = create_app(BaseConfig)
        
    def populate_table(self, model, filename):
        records = []
        with open(f'{BASE_DIR}/tests/db_fixtures/{filename}') as f:
            for line in f.readlines():
                records.append(json.loads(line))

        for record in records:
            result = model.record_from_dict(record)  # TODO: program a record_from_dict func
