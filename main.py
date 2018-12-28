from config import BaseConfig

from base_project import create_app


def app():
    app = create_app(BaseConfig)

    return app