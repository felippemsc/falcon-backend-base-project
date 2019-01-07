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
        message = {
            "message": "Measuring distance",
            "duration": 5,
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headears}
        )

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual(message, response.json.get("message"))
