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

    def test_get_collection_unauthorized(self):
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

    def test_get_resource_unauthorized(self):
        response = self.simulate_get(f'{self.endpoint}/1', headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_get_resource(self):
        response = self.simulate_get(f'{self.endpoint}/1',
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("message", response.json)

    def test_get_resource_not_found(self):
        response = self.simulate_get(f'{self.endpoint}/999',
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_delete_unauthorized(self):
        response = self.simulate_delete(f'{self.endpoint}/1', headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_delete(self):
        response = self.simulate_delete(f'{self.endpoint}/1',
                                        headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("msg", response.json)
        self.assertIn("message", response.json)

    def test_delete_invalid_id(self):
        response = self.simulate_delete(f'{self.endpoint}/999',
                                        headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_patch_unauthorized(self):
        response = self.simulate_patch(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_patch_successful(self):
        message = {
            "message": "Patch Test",
            "duration": 999
        }

        response = self.simulate_patch(
            f'{self.endpoint}/1', json=message, headers={**self.headers,
                                                         **{'Authorization': encode_base_auth_header('xpto')}}
        )

        resp_message = response.json.get('message')

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual("Patch Test", resp_message.get('message'))
        self.assertEqual(999, resp_message.get('duration'))
        self.assertEqual("Information", resp_message.get('message_category'))

        message = {
            "duration": 123
        }

        response = self.simulate_patch(
            f'{self.endpoint}/1', json=message, headers={**self.headers,
                                                         **{'Authorization': encode_base_auth_header('xpto')}}
        )

        resp_message = response.json.get('message')

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual("Patch Test", resp_message.get('message'))
        self.assertEqual(123, resp_message.get('duration'))
        self.assertEqual("Information", resp_message.get('message_category'))

    def test_patch_invalid_id(self):
        message = {
            "message": "Patch Test",
            "duration": 999
        }

        response = self.simulate_patch(
            f'{self.endpoint}/999', json=message, headers={**self.headers,
                                                           **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_patch_invalid_field(self):
        message = {
            "duration": "5",
            "message_category": "Information"
        }

        response = self.simulate_patch(
            f'{self.endpoint}/1', json=message, headers={**self.headers,
                                                         **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.json)

    def test_patch_message_already_exists(self):
        message = {
            "message": "Welcome to IoT",
            "duration": 5
        }

        response = self.simulate_patch(
            f'{self.endpoint}/2', json=message, headers={**self.headers,
                                                         **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_BAD_REQUEST)
        self.assertIn("description", response.json)

    # TODO: improve the test patch
