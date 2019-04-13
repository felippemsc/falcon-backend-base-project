# coding: utf-8
"""
Base Models

Author: Felippe Costa <felippemsc@gmail.com>
"""
from datetime import datetime

from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.collections import InstrumentedList

from ..database import BASE, DBSESSION

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


class BaseModel(AbstractConcreteBase, BASE):
    """
    Base Model
    """
    _json_schema = None
    _query_schema = None
    __tablename__ = None
    serializer_fields = None

    @classmethod
    def validate_and_init(cls, data: dict):
        """
        Validates and instantiates an object class using the dict values.

        :param data: dictionary with data
        :return: instantiated object
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
        :param data: dictionary with data
        :return: instantiated object
        """
        instance = cls.validate_and_init(data)

        instance.commit()
        return instance

    def validate_and_update(self, data: dict):
        """
        Validates and updates a new registry
        :param data: dictionary with data
        :return: instantiated object
        """
        self._json_schema.validate(data, drop_required_fields=True)

        for key in data:
            model_att = getattr(self.__class__, key, None)
            value = data.get(key)

            setattr(self, key, type(model_att.type.python_type())(value))

        self.commit()

    @classmethod
    def get_list(cls, url_params: dict):
        """
        Retrieves the records of a model's table paginated with limit and
        offset

        :return: serialized list of instances
        """
        cls._query_schema.validate(url_params)

        limit = url_params.get('limit')
        offset = url_params.get('offset')

        if limit is None or int(limit) > 100:
            limit = 100

        instance_list = DBSESSION.query(cls)
        instance_list = instance_list.order_by(cls.id)
        instance_list = instance_list.offset(offset)
        instance_list = instance_list.limit(limit)
        instance_list = instance_list.all()

        return cls.serialize_list(instance_list)

    @classmethod
    def get_by_id(cls, id_: int):
        """
        Retrieves a record by its id

        :param id_:
        :return: serialized instance
        """
        query = DBSESSION.query(cls)
        instance = query.get(id_)
        return instance

    @staticmethod
    def serialize_list(list_of_instances: list,
                       serialize_children: bool = False,
                       drop_parents: bool = False):
        """
        Serializes a list of instances

        :param list_of_instances: list of the instances to be serialized
        :param serialize_children: if the children relationships should be
                                   serialized
        :param drop_parents: if the parents relationships should be dropped
                             on the serialization
        :return: list of dicts
        """
        serialized_list = []
        for instance in list_of_instances:
            serialized_list.append(instance.serialize(serialize_children,
                                                      drop_parents))

        return serialized_list

    def serialize(self, serialize_children: bool = False,
                  drop_parents: bool = False):
        """
        Serialize an instance of a model record

        :param serialize_children: if serializes the children relationships
                                   or not
        :param drop_parents: if drops the parents relationships or not
        :return: dict
        """
        result = dict()

        for key in self.serializer_fields:
            inst_value = getattr(self, key, None)

            if isinstance(inst_value, datetime):
                inst_value = inst_value.strftime(DATETIME_FORMAT)
            if isinstance(inst_value, InstrumentedList):
                if serialize_children:
                    inst_value = BaseModel.serialize_list(inst_value,
                                                          drop_parents=True)
                else:
                    continue
            if isinstance(inst_value, BaseModel):
                if not drop_parents:
                    inst_value = inst_value.serialize(False)
                else:
                    continue

            result[key] = inst_value

        return result

    def commit(self):
        """
        Commit a record to the database
        """
        try:
            DBSESSION.add(self)
            DBSESSION.commit()
        except IntegrityError:
            DBSESSION.rollback()
            raise

    def delete(self):
        """
        Deletes a record from the database
        """
        DBSESSION.delete(self)
        DBSESSION.commit()
