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


def create_database_if_needed(db_uri):
    """
    Cria o banco de dados, se necessário.
    """
    if not database_exists(db_uri):
        LOG.info('Banco de dados inexistente. Iniciando criação...')
        try:
            create_database(db_uri)
        except Exception:
            LOG.exception('Erro ao criar o Banco de Dados: ')
            raise


def init_db(db_uri):
    """
    Configura o acesso ao banco de dados.
    """
    # LOG.info(f"Conectando ao banco de dados '{db_uri}'.")

    engine = create_engine(db_uri)

    DBSESSION.remove()
    DBSESSION.configure(
        bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)

    BASE.metadata.create_all(engine)

    return engine


def reset_db(db_uri):
    """
    Reinicializa o banco de dados.
    """
    try:

        engine = init_db(db_uri)
        BASE.metadata.drop_all(engine)
        BASE.metadata.create_all(engine)
        # logging.info('Banco de Dados reinicializado com sucesso.')
    except Exception:
        LOG.exception('Erro ao criar o Banco de Dados: ')


def create_schema():
    """
    Cria o schema conta_corrente no banco e impede o problema nos testes.
    """
    DBSESSION.execute('CREATE SCHEMA IF NOT EXISTS base_schema')
    DBSESSION.commit()
