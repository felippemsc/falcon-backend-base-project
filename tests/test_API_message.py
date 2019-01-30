# coding=utf-8
from falcon import HTTP_CREATED, HTTP_UNPROCESSABLE_ENTITY

from tests import BaseTest, encode_base_auth_header


class TestAPIMessage(BaseTest):
    endpoint = '/message'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def setUp(self):
        super().setUp()

        # self.populate_table() TODO

    def test_unauthenticated(self):
        response = self.simulate_post(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_post(self):
        message = {
            "message": "Measuring distance",
            "duration": 5,
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headers,
                                                  **{'Authorization': encode_base_auth_header('xpto')}}
        )

        resp_message = response.json.get('message')

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual("Measuring distance", resp_message.get('message'))
        self.assertEqual(5, resp_message.get('duration'))
        self.assertEqual("Information", resp_message.get('message_category'))

    def test_post_failed_schema(self):
        message = {
            "duration": 5,
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headers,
                                                  **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        #
        # self.assertEqual(response.status, HTTP_CREATED)
        # self.assertEqual("Measuring distance", resp_message.get('message'))
        # self.assertEqual(5, resp_message.get('duration'))
        # self.assertEqual("Information", resp_message.get('message_category'))
