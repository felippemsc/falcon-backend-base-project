import logging

import falcon


class InvalidJSON(Exception):
    """
    Exception for invalid JSON Schema
    """
    @staticmethod
    def handle(ex, req, resp, params):
        """
        Removes the active session, doing rollback
        if the request was not successful
        """
        logger = logging.getLogger()
        if not isinstance(ex, InvalidJSON):
            logger.exception("Unexpected Error: ")
            ex = falcon.HTTPInternalServerError(description=str(ex))
        else:
            ex = falcon.HTTPUnprocessableEntity(description=str(ex))
        raise ex
