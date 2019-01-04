# coding: utf-8
"""
Message's View

Author: Felippe Costa <felippemsc@orama.com>
"""
import json
import logging

from falcon import HTTP_CREATED

from ..models.message import MessageModel
from ..schema.json_schema import SchemaMessage


LOG = logging.getLogger()

# pylint: disable=W0511
# TODO: Create MessageResource and create middleware for auth


class MessageCollection:
    """
    API for the Collection of Messages
    """
    def on_post(self, request, response):
        """
        API to create new Messages
        """
        payload = request.media

        # TODO: Change the validate to a serialize,
        # TODO: that will do the validation also and return an initialized model object
        # TODO: SAVE

        aaa = MessageModel.serialize(payload)

        response.status = HTTP_CREATED
        response.body = json.dumps({"payload": payload})
