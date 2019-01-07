# coding: utf-8
"""

Base Models

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.exc import IntegrityError

from ..database import BASE, DBSESSION

LOG = logging.getLogger(__name__)


class BaseModel(AbstractConcreteBase, BASE):
    """
    Base Model
    """
    __json_schema = None
    __tablename__ = None

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
        if result:
            return instance

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
        except Exception as err:
            aa = 2
