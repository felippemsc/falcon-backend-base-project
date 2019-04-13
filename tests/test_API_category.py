# coding=utf-8
import logging

from falcon import HTTP_CREATED, HTTP_UNPROCESSABLE_ENTITY, HTTP_BAD_REQUEST, HTTP_OK, HTTP_NOT_FOUND

from base_project.models.category import Category
from base_project.models.message import Message

from tests import BaseTest, encode_base_auth_header

LOG = logging.getLogger()


class TestAPICategory(BaseTest):
    endpoint = '/category'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    def setUp(self):
        super().setUp()

        self.populate_table(Category, 'category.jsonl')
        self.populate_table(Message, 'message.jsonl')

    def test_post_unauthorized(self):
        response = self.simulate_post(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_post_missing_required_fields(self):
        category = {
            "test": "test"
        }

        response = self.simulate_post(
            self.endpoint, json=category, headers={**self.headers,
                                                   **{'Authorization': encode_base_auth_header('xpto')}}
        )
        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.json)

    def test_post_invalid_field(self):
        category = {
            "name": 1
        }

        response = self.simulate_post(
            self.endpoint, json=category, headers={**self.headers,
                                                   **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.json)

    def test_post_category_already_exists(self):
        category = {
            "name": "Information"
        }

        response = self.simulate_post(
            self.endpoint, json=category, headers={**self.headers,
                                                   **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_BAD_REQUEST)
        self.assertIn("description", response.json)

    def test_post_successful(self):
        category = {
            "name": "Error"
        }

        response = self.simulate_post(
            self.endpoint, json=category, headers={**self.headers,
                                                   **{'Authorization': encode_base_auth_header('xpto')}}
        )

        resp_category = response.json.get('category')

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual("Error", resp_category.get('name'))
        self.assertEqual(3, resp_category.get('id'))

    def test_get_collection_unauthorized(self):
        response = self.simulate_get(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_get_collection(self):
        response = self.simulate_get(self.endpoint, headers={**self.headers,
                                                             **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("categories", response.json)
        self.assertEqual(2, len(response.json.get('categories')))

        category = {
            "name": "Error"
        }

        response = self.simulate_post(
            self.endpoint, json=category, headers={**self.headers,
                                                   **{'Authorization': encode_base_auth_header('xpto')}}
        )
        self.assertEqual(response.status, HTTP_CREATED)

        response = self.simulate_get(self.endpoint, headers={**self.headers,
                                                             **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("categories", response.json)
        self.assertEqual(3, len(response.json.get('categories')))

    def test_get_collection_limit(self):
        response = self.simulate_get(self.endpoint, query_string="limit=1",
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("categories", response.json)
        self.assertEqual(1, len(response.json.get('categories')))

    def test_get_collection_offset(self):
        response = self.simulate_get(self.endpoint, query_string="offset=0",
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("categories", response.json)
        self.assertEqual(2, len(response.json.get('categories')))

    def test_get_collection_not_found(self):
        response = self.simulate_get(self.endpoint, query_string="offset=2",
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_NOT_FOUND)
        self.assertIn("categories", response.json)
        self.assertEqual(0, len(response.json.get('categories')))

    def test_get_resource_unauthorized(self):
        response = self.simulate_get(f'{self.endpoint}/1', headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_get_resource(self):
        response = self.simulate_get(f'{self.endpoint}/1',
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("category", response.json)

    def test_get_resource_not_found(self):
        response = self.simulate_get(f'{self.endpoint}/999',
                                     headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_delete_unauthorized(self):
        response = self.simulate_delete(f'{self.endpoint}/1', headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_delete(self):
        response = self.simulate_delete(f'{self.endpoint}/2',
                                        headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_OK)
        self.assertIn("msg", response.json)
        self.assertIn("category", response.json)

    def test_delete_used_category(self):
        response = self.simulate_delete(f'{self.endpoint}/1',
                                        headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_BAD_REQUEST)
        self.assertIn("description", response.json)

    def test_delete_invalid_id(self):
        response = self.simulate_delete(f'{self.endpoint}/999',
                                        headers={**self.headers, **{'Authorization': encode_base_auth_header('xpto')}})

        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_patch_unauthorized(self):
        response = self.simulate_patch(self.endpoint, headers={**self.headers})

        self.assertEqual(401, response.status_code)

    def test_patch_successful(self):
        category = {
            "name": "Error"
        }

        response = self.simulate_patch(
            f'{self.endpoint}/2', json=category, headers={**self.headers,
                                                          **{'Authorization': encode_base_auth_header('xpto')}}
        )

        resp_category = response.json.get('category')

        self.assertEqual(response.status, HTTP_CREATED)
        self.assertEqual("Error", resp_category.get('name'))

    def test_patch_used_category(self):
        category = {
            "name": "Error"
        }

        response = self.simulate_patch(
            f'{self.endpoint}/1', json=category, headers={**self.headers,
                                                          **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_BAD_REQUEST)
        self.assertIn("description", response.json)

    def test_patch_invalid_id(self):
        category = {
            "name": "Error"
        }

        response = self.simulate_patch(
            f'{self.endpoint}/999', json=category, headers={**self.headers,
                                                           **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_NOT_FOUND)

    def test_patch_invalid_field(self):
        category = {
            "name": 1
        }

        response = self.simulate_patch(
            f'{self.endpoint}/2', json=category, headers={**self.headers,
                                                          **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_UNPROCESSABLE_ENTITY)
        self.assertIn("description", response.json)

    def test_patch_category_already_exists(self):
        category = {
            "name": "Information"
        }

        response = self.simulate_patch(
            f'{self.endpoint}/2', json=category, headers={**self.headers,
                                                         **{'Authorization': encode_base_auth_header('xpto')}}
        )

        self.assertEqual(response.status, HTTP_BAD_REQUEST)
        self.assertIn("description", response.json)
