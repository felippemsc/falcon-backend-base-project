#!/usr/bin/env python
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()

requires = [
    'astroid==2.2.0',
    'click==6.7',
    'falcon==1.4.1',
    'gunicorn==19.9.0',
    'jsonschema==2.6.0',
    'pycodestyle==2.3.1',
    'pylint==2.3.0',
    'psycopg2-binary==2.7.6.1',
    'simple_json_log_formatter==0.5.3',
    'SQLAlchemy==1.2.15',
    'SQLAlchemy-Utils==0.33.10'
]

tests_require = [
    'docker-compose',
    'gunicorn==19.9.0',
    'pytest==4.0.2',
    'pytest-codestyle==1.4.0',
    'pytest-cov==2.6.0',
    'pytest-pylint==0.13.0'
]

setup_requires = ['pytest-runner']


setup(
    name=u"Falcon Base Project",
    version="1.0.0",
    description=u"This is a base backend project using the falcon webframework",
    long_description=long_description,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Falcon',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Felippe Costa',
    author_email='felippemsc@gmail.com',
    python_requires='>=3.7',
    packages=find_packages(exclude='tests'),
    install_requires=requires,
    test_suite='tests',
    setup_requires=setup_requires,
    tests_require=tests_require
)