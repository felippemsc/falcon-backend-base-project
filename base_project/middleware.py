# coding: utf-8
"""
Middleware module

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

import falcon

from .schema.json_schema import InvalidJSON

from .database import DBSESSION

LOG = logging.getLogger(__name__)


class SQLAlchemySessionManager:
    """
    Removes the SQLAlchemy's Session after each request.
    """
    # pylint: disable=W0613
    def process_response(self, req, resp, resource, req_succeeded):
        """
        Removes the active session, doing rollback
        if the request was not successful
        """
        if not req_succeeded:
            DBSESSION.rollback()
        DBSESSION.remove()


class CheckAuth:
    """
    Checks the Authorization before each request.
    """
    def process_request(self, req, resp):  # pylint: disable=W0613
        """Process the request, checking if AUTHORIZATION is in the headers"""
        if req.relative_uri == '/':
            return

        if 'AUTHORIZATION' not in req.headers:
            raise falcon.HTTPUnauthorized()
