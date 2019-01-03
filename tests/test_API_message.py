# coding=utf-8
from falcon import HTTP_CREATED

from tests import BaseTest


class TestAPIMessage(BaseTest):
    endpoint = '/message'
    headears = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def setUp(self):
        super().setUp()

        # self.populate_table() TODO

    def test_post(self):
        payload = {"test": "SUCCESS"}

        response = self.simulate_post(
            self.endpoint, json=payload, headers={**self.headears}
        )

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual("SUCCESS", response.json.get("payload").get("test"))
