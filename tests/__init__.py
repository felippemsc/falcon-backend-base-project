import os

from falcon import testing

from config import BaseConfig

from base_project import create_app


class BaseTest(testing.TestCase):
    """
    Main class for unit tests
    """
    dir_ = os.path.dirname(__file__)

    def setUp(self):
        """Configure what is necessary for the tests."""
        super().setUp()

        self.app = create_app(BaseConfig)
