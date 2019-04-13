# coding: utf-8
"""
Exceptions module

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

import falcon

from sqlalchemy.exc import IntegrityError

from .schema.json_schema import InvalidJSON
from .middleware import UnauthorizedException
from .models.category import ProtectedCategory


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
        # TODO: Improve and check the log messages
        logger = logging.getLogger()
        log_msg = f"{req.method} for {req.relative_uri} {cls.get_payload(req)}"

        if isinstance(ex, InvalidJSON):
            logger.exception("Error with the json schema during handling the %s: ", log_msg)  # noqa
            ex = falcon.HTTPUnprocessableEntity(description=str(ex))
        elif isinstance(ex, UnauthorizedException):
            logger.exception("Unauthorized Error of request on %s: ", log_msg)
            ex = falcon.HTTPUnauthorized(description=str(ex))
        elif isinstance(ex, IntegrityError):
            logger.exception("Database integrity error violation when handling %s: %s", log_msg, str(ex.orig.pgerror))  # noqa
            ex = falcon.HTTPBadRequest(description="Database integrity error violation")  # noqa
        elif isinstance(ex, ProtectedCategory):
            logger.exception("Cannot update/delete this record of Category %s: ", log_msg)  # noqa
            ex = falcon.HTTPBadRequest(description=str(ex))
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
        except falcon.HTTPBadRequest:
            payload_msg = "without payload"

        return payload_msg
# pylint: enable=C0301
