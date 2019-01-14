# coding=utf-8
from falcon import HTTP_OK

from tests import BaseTest


class TestAPIRoot(BaseTest):
    def test_root(self):
        response = self.simulate_get('/')

        self.assertEqual(response.status, HTTP_OK)
