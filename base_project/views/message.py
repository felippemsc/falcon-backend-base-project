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

# TODO: Create MessageResource


class MessageCollection:
    """
    API for the Collection of Messages
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
