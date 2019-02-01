# coding: utf-8
"""Module database

Author: Felippe Costa <felippemsc@gmail.com>
"""
import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


META = MetaData(schema="base_schema")
BASE = declarative_base(metadata=META)
DBSESSION = scoped_session(sessionmaker())


LOG = logging.getLogger(__name__)


def init_db(db_uri):
    """
    Configures the access to the database.
    """
    engine = create_engine(db_uri)

    DBSESSION.remove()
    DBSESSION.configure(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

    BASE.metadata.create_all(engine)

    return engine


def create_database_if_needed(db_uri):
    """
    Create database if necessary.
    """
    if not database_exists(db_uri):
        LOG.info('Nonexistent Database. Creating...')
        try:
            create_database(db_uri)
        except Exception:
            LOG.exception('Error at creating the Database: ')
            raise


def init_db_local(db_uri):
    """
    Create local db
    """
    create_database_if_needed(db_uri)
    engine = create_engine(db_uri)

    DBSESSION.remove()
    DBSESSION.configure(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

    DBSESSION.execute('CREATE SCHEMA IF NOT EXISTS base_schema')
    DBSESSION.commit()

    BASE.metadata.create_all(engine)
    return engine


def reset_db_for_testing(db_uri):
    """
    Resets the db for the tests.
    """
    try:
        engine = init_db_local(db_uri)
        BASE.metadata.drop_all(engine)
        BASE.metadata.create_all(engine)
    except Exception:
        LOG.exception('Error at creating the Database: ')
