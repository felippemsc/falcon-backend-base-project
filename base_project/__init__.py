# coding: utf-8
"""
App creation

Author: Felippe Costa <felippemsc@gmail.com>
"""
import falcon
from .views import RootResource
from .views.message import MessageCollection


# Use the app_settings to create the db connection, TODO
# erase the pylint disable bellow TODO
def create_app(app_settings):  # pylint: disable=W0613
    """
    Application factory

    :param app_settings: a configuration object
    :return: An application Falcon object
    """
    # Application inicialization
    app = falcon.API()

    # APIs
    app.add_route('/', RootResource())
    app.add_route('/message', MessageCollection())

    return app
