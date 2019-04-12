# coding: utf-8
"""Module category

ORM of Base Project: category model.

Author: Felippe Costa <felippemsc@gmail.com>
"""
from sqlalchemy import Integer, Text
from sqlalchemy.schema import Column

from ..models import BaseModel
from ..schema.json_schema import SchemaBaseQuery, SchemaCategory

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class Category(BaseModel):
    """
    Category's Model
    """
    _json_schema = SchemaCategory
    _query_schema = SchemaBaseQuery
    __tablename__ = 'category'
    serializer_fields = [
        "id", "name"
    ]

    id = Column("id_category", Integer, primary_key=True, autoincrement=True)
    name = Column("nm_category", Text, nullable=False, unique=True)
