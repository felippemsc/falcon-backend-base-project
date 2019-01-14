# coding: utf-8
"""

Base Models

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging
from datetime import datetime, date
from decimal import Decimal

from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.exc import IntegrityError

from ..database import BASE, DBSESSION

LOG = logging.getLogger(__name__)

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class BaseModel(AbstractConcreteBase, BASE):
    """
    Base Model
    """
    __json_schema = None
    __tablename__ = None
    serializer_fields = None

    @classmethod
    def validate_and_init(cls, data: dict):
        """
        Validates and instancieates an object class using the dict values.

        :param data: dictonary with data
        :return: instanciated object
        """
        cls._json_schema.validate(data)
        instance = cls()
        for key in data:
            model_att = getattr(instance.__class__, key, None)
            value = data.get(key)

            setattr(instance, key, type(model_att.type.python_type())(value))

        return instance

    @classmethod
    def validate_and_record(cls, data: dict):
        """
        Validates and record a new registry
        :param data: dictonary with data
        :return: instanciated object
        """
        instance = cls.validate_and_init(data)

        result = instance.commit()
        if not result:
            msg = 'Unexpected trouble when commiting record to the database.'
            LOG.exception(msg)
            raise Exception(msg)

        return instance

    def serialize(self):
        """
        Serialize an instance of a model record

        :return: dict
        """
        result = dict()

        for key in self.serializer_fields:
            instance_value = getattr(self, key, None)

            if isinstance(instance_value, datetime):
                instance_value = instance_value.strftime(DATETIME_FORMAT)
            if isinstance(instance_value, date):
                instance_value = instance_value.strftime(DATE_FORMAT)
            if isinstance(instance_value, Decimal):
                instance_value = str(instance_value)

            result[key] = instance_value

        return result

    def commit(self):
        """
        Commit a record to the database
        """
        try:
            DBSESSION.add(self)
            DBSESSION.commit()

            return True
        except IntegrityError:
            LOG.exception("Integrity Violation: ")
            DBSESSION.rollback()
            raise
