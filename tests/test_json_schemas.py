# coding=utf-8
import logging

from base_project.schema.json_schema import Schema, InvalidJSON

from tests import BaseTest

LOG = logging.getLogger()


class TestJSONSchema(BaseTest):

    def setUp(self):
        super().setUp()

    def test_schema_without_dict(self):
        class TestSchema(Schema):
            schema_dict = None

        try:
            TestSchema.validate({"test": "test"})
        except Exception as err:
            self.assertEqual(str(err), "JSON Schema not defined for the class 'TestSchema'")

    def test_invalid_schema(self):
        class TestSchema(Schema):
            schema_dict = {
                "$json_schema": "http://json-json_schema.org/json_schema#",
                "type": "object",
                "properties": {
                    "test": {"type": ""}
                }
            }

        try:
            TestSchema.validate({"test": "test"})
        except Exception as err:
            self.assertTrue(isinstance(err, InvalidJSON))
