# coding: utf-8
"""Module message

ORM of Base Project: message model.

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

from sqlalchemy import Integer, Text, DateTime, Boolean, String, func
from sqlalchemy.schema import Column
from sqlalchemy.ext.declarative import AbstractConcreteBase

from ..database import BASE, DBSESSION

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


LOG = logging.getLogger(__name__)


class MessageModel(AbstractConcreteBase, BASE):
    """
    Messages
    """
    __tablename__ = 'message'
    id = Column("id_message", Integer, primary_key=True, autoincrement=True)
    message = Column("message", Text, nullable=False)
    duration = Column("dur_message", Integer, nullable=True)
    creation_date = Column("dh_message", DateTime, default=func.now())
    message_category = Column("cat_message", String(5), nullable=False)
    printed_times = Column("prt_message", Integer, default=0)
    printed_once = Column("bol_message", Boolean, default=False)
