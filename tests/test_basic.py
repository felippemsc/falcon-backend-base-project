# coding=utf-8
import falcon
import logging

from unittest.mock import patch

from sqlalchemy.exc import NoSuchModuleError

from base_project.exception_handler import ExceptionHandler
from base_project.database import reset_db_for_testing, create_database_if_needed

from tests import BaseTest, TestLogger

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


class TestDatabaseModule(TestLogger):
    """
    Class for testing the database interactions
    """
    def setUp(self):
        """Configure what is necessary for the tests."""
        super().setUp()
        self.set_logging()

    @patch('base_project.database.database_exists')
    def test_init_db(self, mock_database_exists):
        mock_database_exists.return_value = False
        try:
            create_database_if_needed('abc://xyz:123@localhost:5432/ijk')
        except Exception as err:
            self.assertTrue(isinstance(err, NoSuchModuleError))

    def test_reset_db(self):
        try:
            reset_db_for_testing('abc://xyz:123@localhost:5432/ijk')
        except Exception as err:
            self.assertTrue(isinstance(err, NoSuchModuleError))


