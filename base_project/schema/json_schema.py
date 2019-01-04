# coding: utf-8
"""Module json_schema

JSON Schemas.

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

from jsonschema import validate as json_schema_validate
from jsonschema.exceptions import SchemaError, ValidationError


LOG = logging.getLogger(__name__)


class InvalidJSON(Exception):
    """Exception for invalid JSON Schema"""
    pass


class Schema:
    """
    Root class for the JSON Schema validation
    """
    schema_dict = None

    @classmethod
    def validate(cls, record: dict):
        """
        Validate a record (json or dict) against a json schema.

        :param record: dict of values
        """
        schema_dict = cls.schema_dict
        if schema_dict is None:
            raise InvalidJSON(f"JSON Schema not defined for the class '{cls.__name__}'")

        try:
            json_schema_validate(record, schema_dict)
            return
        except SchemaError as err:
            LOG.exception("Error on the schema: ")
            raise InvalidJSON(f"JSON Schema '{cls.schema_dict}', of class '{cls.__name__}', is invalid: '{err}'.")
        except ValidationError as err:
            LOG.exception("Error on the validation: ")
            raise InvalidJSON(f"Record '{record}' is not valid: '{err}'.")


class SchemaMessage(Schema):
    """
    JSON Schema that represents a Message.
    """
    schema_dict = {
        "$json_schema": "http://json-json_schema.org/json_schema#",
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "message": {"type": "string"},
            "duration": {"type": ["integer", "null"]},
            "message_category": {"type": "string"},
            "printed_times": {"type": "integer"},
            "printed_once": {"type": "boolean"},
        },
        "required": [
            "message", "message_category"
        ]
    }