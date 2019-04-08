# coding=utf-8
import falcon
import logging

from falcon import testing
from sqlalchemy.exc import NoSuchModuleError

from base_project.exception_handler import ExceptionHandler
from base_project.database import reset_db_for_testing

from tests import BaseTest

LOG = logging.getLogger()


class TestAPIRoot(BaseTest):
    def test_healthcheck(self):
        response = self.simulate_get('/')

        self.assertEqual(response.status, falcon.HTTP_OK)


class TestExceptionHandler(BaseTest):
    def test_exception_handler(self):
        class FakeRequest:
            def __init__(self):
                self.method = 'FAKE_POST'
                self.relative_uri = '/fake-uri'
                self.media = '{"test": "test"}'

        try:
            ExceptionHandler.handle(Exception, FakeRequest(), "response", "anything")
        except Exception as err:
            self.assertTrue(isinstance(err, falcon.HTTPInternalServerError))


class TestDatabase(testing.TestCase):
    """
    Class for testing the database interactions
    """
    tests_handler = BaseTest.tests_handler
    logging.basicConfig(
        format=("\n%(asctime)s [%(levelname)s] "
                "[%(module)s:%(funcName)s:%(lineno)s] "
                "[%(threadName)s-%(thread)d] \n%(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S")

    def set_logging(self):
        """
        Configures the log for testing.

        To cleanner output the level is set to the highest.

        Level could be changed for more details during the tests.

        It is possible to override this fucntion to change the log level for specific tests.
        """
        LOG.level = logging.CRITICAL
        LOG.addHandler(self.tests_handler)

    def setUp(self):
        """Configure what is necessary for the tests."""
        super().setUp()
        self.set_logging()

    # TODO: create the test for initing the db (mock database_exists and create_database)
    def test_init_db(self):
        pass

    def test_reset_db(self):
        try:
            reset_db_for_testing('abc://xyz:123@localhost:5432/ijk')
        except Exception as err:
            self.assertTrue(isinstance(err, NoSuchModuleError))


