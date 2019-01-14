# coding: utf-8
"""
Message's View

Author: Felippe Costa <felippemsc@orama.com>
"""
import json
import logging

from falcon import HTTP_CREATED

from ..models.message import MessageModel


LOG = logging.getLogger()

# pylint: disable=W0511
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

        message = MessageModel.validate_and_record(payload)

        response.status = HTTP_CREATED
        response.body = json.dumps({"message": message.serialize()})
