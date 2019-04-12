# coding: utf-8
"""Module message

ORM of Base Project: message model.

Author: Felippe Costa <felippemsc@gmail.com>
"""
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship, backref

from ..models import BaseModel
from ..schema.json_schema import SchemaBaseQuery, SchemaMessage

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class Message(BaseModel):
    """
    Message's Model
    """
    _json_schema = SchemaMessage
    _query_schema = SchemaBaseQuery
    __tablename__ = 'message'
    serializer_fields = [
        "id", "message", "duration", "creation_date", "category_id",
        "printed_times", "printed_once"
    ]

    id = Column("id_message", Integer, primary_key=True, autoincrement=True)
    message = Column("message", Text, nullable=False, unique=True)
    duration = Column("dur_message", Integer, nullable=True)
    creation_date = Column("dh_message", DateTime, default=func.now())
    category_id = Column("id_category_fk", Integer,
                         ForeignKey('category.id_category'), nullable=False)
    printed_times = Column("prt_message", Integer, default=0)
    printed_once = Column("bol_message", Boolean, default=False)

    category = relationship("Category", backref=backref("message",
                                                        lazy="joined"))
