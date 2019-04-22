#!/usr/bin/env bash

sleep 10
python main.py createdb
gunicorn -w 4 -b 0.0.0.0:8080 --log-config logging.ini main:app