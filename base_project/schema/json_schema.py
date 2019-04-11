# coding: utf-8
"""Module json_schema

JSON Schemas.

Author: Felippe Costa <felippemsc@gmail.com>
"""
from jsonschema import validate as json_schema_validate
from jsonschema.exceptions import SchemaError, ValidationError


class InvalidJSON(Exception):
    """Exception raised for invalid json schema"""


class Schema:
    """
    Root class for the JSON Schema validation
    """
    schema_dict = None

    @classmethod
    def validate(cls, record: dict, drop_required_fields: bool = False):
        """
        Validate a record (json or dict) against a json schema.

        :param drop_required_fields: if True drops the required fieds of
                                     the Schema validator
        :param record: dict of values
        """
        if cls.schema_dict is None:
            raise InvalidJSON(f"JSON Schema not defined for the class "
                              f"'{cls.__name__}'")

        schema_dict = cls.schema_dict.copy()
        if drop_required_fields:
            schema_dict.pop("required", None)

        try:
            json_schema_validate(record, schema_dict)
            return
        except SchemaError as err:
            raise InvalidJSON(f"JSON Schema '{cls.schema_dict}', of class "
                              f"'{cls.__name__}', is invalid: '{err}'.")
        except ValidationError as err:
            raise InvalidJSON(f"Record '{record}' is not valid: '{err}'.")


class SchemaBaseQuery(Schema):
    """
    JSON Schema that represents the base query string.
    """
    schema_dict = {
        "$json_schema": "http://json-json_schema.org/json_schema#",
        "type": "object",
        "properties": {
            "limit": {"type": "string"},
            "offset": {"type": "string"},
        }
    }


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


class SchemaCategory(Schema):
    """
    JSON Schema that represents a Message.
    """
    schema_dict = {
        "$json_schema": "http://json-json_schema.org/json_schema#",
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"}
        },
        "required": [
            "name"
        ]
    }
