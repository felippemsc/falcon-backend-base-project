# coding: utf-8
"""
Message's View

Author: Felippe Costa <felippemsc@orama.com>
"""
import json
import logging

from falcon import HTTP_CREATED


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

        response.status = HTTP_CREATED
        response.body = json.dumps({"payload": payload})
