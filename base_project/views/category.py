# coding: utf-8
"""
Category's View

Author: Felippe Costa <felippemsc@orama.com>
"""
import json
import logging

from falcon import HTTP_CREATED, HTTP_NOT_FOUND

from ..models.category import Category

LOG = logging.getLogger()


class CategoryCollection:
    """
    Collection of Messages
    """
    def on_post(self, request, response):
        """
        API to create new Messages
        """
        payload = request.media

        category = Category.validate_and_record(payload)

        response.status = HTTP_CREATED
        response.body = json.dumps({"category": category.serialize()})

    def on_get(self, request, response):
        """
        API to list the messages
        """
        url_params = request.params

        categories = Category.get_list(url_params)
        if not categories:
            response.status = HTTP_NOT_FOUND

        response.body = json.dumps({"categories": categories})


class CategoryResource:
    """
    Resource of a Message
    """
    def on_get(self, request, response, id_):  # pylint: disable=W0613
        """
        API to retrieve one message by its id
        """
        category = Category.get_by_id(id_)
        if not category:
            response.status = HTTP_NOT_FOUND
            return

        response.body = json.dumps(
            {"category": category.serialize(serialize_children=True)})

    def on_delete(self, request, response, id_):  # pylint: disable=W0613
        """
        API to delete one message by its id
        """
        category = Category.get_by_id(id_)
        if not category:
            response.status = HTTP_NOT_FOUND
            return

        category.delete()

        msg = f"Record with id: {id_} was successfully deleted"
        response.body = json.dumps({"msg": msg,
                                    "category": category.serialize()})

    def on_patch(self, request, response, id_):  # pylint: disable=W0613
        """
        API that updates one message by its id
        """
        payload = request.media

        category = Category.get_by_id(id_)
        if not category:
            response.status = HTTP_NOT_FOUND
            return

        category.validate_and_update(payload)

        response.status = HTTP_CREATED
        response.body = json.dumps({"category": category.serialize()})
