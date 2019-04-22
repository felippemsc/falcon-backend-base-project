import click
import logging

from config import BaseConfig

from base_project.database import init_db_local
from base_project import create_app


@click.group()
def cli():
    pass


@cli.command()
def createdb():
    logging.info('Creating the database to run the app locally')
    init_db_local(BaseConfig.DATABASE_URI)


if __name__ == '__main__':
    cli()

app = create_app(BaseConfig)
