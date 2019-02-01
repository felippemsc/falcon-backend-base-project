# coding: utf-8
"""
Exceptions module

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

import falcon

from .schema.json_schema import InvalidJSON

from .middleware import UnauthorizedException
from .models import CommitException


# pylint: disable=C0301
class ExceptionHandler(Exception):
    """
    Exception for invalid JSON Schema
    """
    @classmethod
    def handle(cls, ex, req, resp, params):  # pylint: disable=W0613
        """
        Removes the active session, doing rollback
        if the request was not successful
        """
        logger = logging.getLogger()
        log_msg = f"{req.method} for {req.relative_uri} {cls.get_payload(req)}"

        if isinstance(ex, InvalidJSON):
            logger.exception("Error with the json schema during handling the %s: ", log_msg)  # noqa
            ex = falcon.HTTPUnprocessableEntity(description=str(ex))
        elif isinstance(ex, UnauthorizedException):
            logger.exception("Unauthorized Error of request on %s: ", log_msg)
            ex = falcon.HTTPUnauthorized(description=str(ex))
        elif isinstance(ex, CommitException):
            logger.exception("Error during the commit when handling %s", log_msg)  # noqa
            ex = falcon.HTTPInternalServerError()
        else:
            logger.exception("Unexpected Error during handling the %s: ", log_msg)  # noqa
            ex = falcon.HTTPInternalServerError()
        raise ex

    @staticmethod
    def get_payload(req):
        """Gets the payload string"""
        try:
            payload = req.media
            payload_msg = f"with payload: {payload}"
        except Exception:
            payload_msg = "without payload"

        return payload_msg
# pylint: enable=C0301
