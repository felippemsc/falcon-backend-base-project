# coding: utf-8
"""Module message

ORM of Base Project: message model.

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

from sqlalchemy import Integer, Text, DateTime, Boolean, func
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import AbstractConcreteBase

from ..database import BASE
from ..schema.json_schema import SchemaMessage

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


LOG = logging.getLogger(__name__)


# pylint: disable=W0511
class MessageModel(AbstractConcreteBase, BASE):
    """
    Messages
    """
    __json_schema = SchemaMessage
    __tablename__ = 'message'
    id = Column("id_message", Integer, primary_key=True, autoincrement=True)
    message = Column("message", Text, nullable=False)
    duration = Column("dur_message", Integer, nullable=True)
    creation_date = Column("dh_message", DateTime, default=func.now())
    message_category = Column("cat_message", Text, nullable=False)
    printed_times = Column("prt_message", Integer, default=0)
    printed_once = Column("bol_message", Boolean, default=False)

    @classmethod
    def serialize(cls, data: dict):
        """
        Instancieates an object class using the dict values.

        :param data: dictonary with data
        :return: intanciated object
        """
        cls.__json_schema.validate(data)
        instance = cls()
        for key in data:
            model_att = getattr(instance.__class__, key, None)
            value = data.get(key)

            setattr(instance, key, type(model_att.type.python_type())(value))

        return instance
    # TODO: Program init_from_dict and record_from_dict and
    # TODO: put in the BaseModel
