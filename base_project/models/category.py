# coding: utf-8
"""Module category

ORM of Base Project: category model.

Author: Felippe Costa <felippemsc@gmail.com>
"""
from sqlalchemy import Integer, Text
from sqlalchemy.schema import Column

from ..models import BaseModel
from ..models.message import Message
from ..schema.json_schema import SchemaBaseQuery, SchemaCategory

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class ProtectedCategory(Exception):
    """Exception raised for when a Record of Category is already being used"""


class Category(BaseModel):
    """
    Category's Model
    """
    _json_schema = SchemaCategory
    _query_schema = SchemaBaseQuery
    __tablename__ = 'category'
    serializer_fields = [
        "id", "name", "messages"
    ]

    id = Column("id_category", Integer, primary_key=True, autoincrement=True)
    name = Column("nm_category", Text, nullable=False, unique=True)

    def is_used(self):
        """
        Check if the category record is already used on the message table

        :return: bool
        """
        if not Message.get_by_category(self.id):
            return False
        return True

    def validate_and_update(self, data: dict):
        """
        Override validate_and_update BaseModel method

        Does not allow to update an already used record of Category
        """
        if self.is_used():
            raise ProtectedCategory("Cannot update a record of Category "
                                    "already bound to another Message")
        super().validate_and_update(data)

    def delete(self):
        """
        Override delete BaseModel method

        Does not allow to delete an already used record of Category
        """
        if self.is_used():
            raise ProtectedCategory("Cannot delete a record of Category "
                                    "already bound to another Message")
        super().delete()
