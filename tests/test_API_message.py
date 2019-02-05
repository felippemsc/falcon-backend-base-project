# coding=utf-8
import logging

from falcon import HTTP_CREATED, HTTP_UNPROCESSABLE_ENTITY, HTTP_BAD_REQUEST, HTTP_OK, HTTP_NOT_FOUND

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

    def test_get_unauthorized(self):
        response = self.simulate_get(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_get_collection(self):
        response = self.simulate_get(self.endpoint, headers={**self.headers,
                                                             **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("messages", response.json)
        self.assertEqual(2, len(response.json.get('messages')))

        message = {
            "message": "Measuring distance",
            "duration": 5,
            "message_category": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=message, headers={**self.headers,
                                                  **{'Authorization': encode_base_auth_header('xpto')}}
        )
        self.assertEqual(response.status, HTTP_CREATED)

        response = self.simulate_get(self.endpoint, headers={**self.headers,
                                                             **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("messages", response.json)
        self.assertEqual(3, len(response.json.get('messages')))

    def test_get_collection_limit(self):
        response = self.simulate_get(self.endpoint, query_string="limit=1",
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("messages", response.json)
        self.assertEqual(1, len(response.json.get('messages')))

    def test_get_collection_offset(self):
        response = self.simulate_get(self.endpoint, query_string="offset=0",
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("messages", response.json)
        self.assertEqual(2, len(response.json.get('messages')))

    def test_get_collection_not_found(self):
        response = self.simulate_get(self.endpoint, query_string="offset=2",
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_NOT_FOUND)
        self.assertIn("messages", response.json)
        self.assertEqual(0, len(response.json.get('messages')))
