# coding: utf-8
"""Module message

ORM of Base Project: message model.

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

from sqlalchemy import Integer, Text, DateTime, Boolean, func
from sqlalchemy.schema import Column

from ..models import BaseModel
from ..schema.json_schema import SchemaMessage

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


LOG = logging.getLogger(__name__)


class MessageModel(BaseModel):
    """
    Message's Model
    """
    _json_schema = SchemaMessage
    __tablename__ = 'message'
    serializer_fields = [
        "id", "message", "duration", "creation_date", "message_category",
        "printed_times", "printed_once"
    ]

    id = Column("id_message", Integer, primary_key=True, autoincrement=True)
    message = Column("message", Text, nullable=False)
    duration = Column("dur_message", Integer, nullable=True)
    creation_date = Column("dh_message", DateTime, default=func.now())
    message_category = Column("cat_message", Text, nullable=False)
    printed_times = Column("prt_message", Integer, default=0)
    printed_once = Column("bol_message", Boolean, default=False)
