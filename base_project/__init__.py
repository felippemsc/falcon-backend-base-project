# coding: utf-8
"""
App creation

Author: Felippe Costa <felippemsc@gmail.com>
"""
import falcon

from .database import init_db
from .exception_handler import ExceptionHandler
from .middleware import SQLAlchemySessionManager, CheckAuth
from .views import RootResource
from .views.message import MessageCollection


def create_app(app_settings):
    """
    Application factory

    :param app_settings: a configuration object
    :return: An application Falcon object
    """
    # Application inicialization
    app = falcon.API(
        middleware=[SQLAlchemySessionManager(), CheckAuth()]
    )
    app.add_error_handler(Exception, ExceptionHandler.handle)

    init_db(app_settings.DATABASE_URI)

    # APIs
    app.add_route('/', RootResource())
    app.add_route('/message', MessageCollection())

    return app
