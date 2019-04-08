# coding: utf-8
"""
Message's View

Author: Felippe Costa <felippemsc@orama.com>
"""
import json
import logging

from falcon import HTTP_CREATED, HTTP_NOT_FOUND

from ..models.message import Message


LOG = logging.getLogger()


class MessageCollection:
    """
    Collection of Messages
    """
    def on_post(self, request, response):
        """
        API to create new Messages
        """
        payload = request.media

        message = Message.validate_and_record(payload)

        response.status = HTTP_CREATED
        response.body = json.dumps({"message": message.serialize()})

    def on_get(self, request, response):
        """
        API to list the messages
        """
        url_params = request.params

        messages = Message.get_list(url_params)
        if not messages:
            response.status = HTTP_NOT_FOUND

        response.body = json.dumps({"messages": messages})


class MessageResource:
    """
    Resource of a Message
    """
    def on_get(self, request, response, id_):  # pylint: disable=W0613
        """
        API to retrieve one message by its id
        """
        message = Message.get_by_id(id_)
        if not message:
            response.status = HTTP_NOT_FOUND
            return

        response.body = json.dumps({"message": message.serialize()})

    def on_delete(self, request, response, id_):  # pylint: disable=W0613
        """
        API to delete one message by its id
        """
        message = Message.get_by_id(id_)
        if not message:
            response.status = HTTP_NOT_FOUND
            return

        message.delete()

        msg = f"Record with id: {id_} was successfully deleted"
        response.body = json.dumps({"msg": msg,
                                    "message": message.serialize()})

    def on_patch(self, request, response, id_):  # pylint: disable=W0613
        """
        API that updates one message by its id
        """
        payload = request.media

        message = Message.get_by_id(id_)
        if not message:
            response.status = HTTP_NOT_FOUND
            return

        message.validate_and_update(payload)

        response.status = HTTP_CREATED
        response.body = json.dumps({"message": message.serialize()})
