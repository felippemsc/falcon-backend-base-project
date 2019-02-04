# coding=utf-8
import logging

from falcon import HTTP_CREATED, HTTP_UNPROCESSABLE_ENTITY, HTTP_BAD_REQUEST

from base_project.models.message import Message

from tests import BaseTest, encode_base_auth_header

LOG = logging.getLogger()


class TestAPIMessage(BaseTest):
    endpoint = '/message'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def setUp(self):
        super().setUp()

        self.populate_table(Message, 'message.jsonl')

    def test_post_unauthorized(self):
        response = self.simulate_post(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_post_missing_required_fields(self):
        message = {
            "duration": 5,
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headers,
                                                  **{'Authorization': encode_base_auth_header('xpto')}}
        )
        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.json)

    def test_post_invalid_field(self):
        message = {
            "message": "Measuring distance",
            "duration": "5",
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headers,
                                                  **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.json)

    def test_post_message_already_exists(self):
        message = {
            "message": "Welcome to IoT",
            "duration": 5,
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headers,
                                                  **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_BAD_REQUEST)
        self.assertIn("description", response.json)

    def test_post_successful(self):
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

    # TODO get collection
    # TODO unauthorized
    # TODO get no results
    # TODO get one result
    # TODO get many results
    # TODO pagination (limit e offset)
