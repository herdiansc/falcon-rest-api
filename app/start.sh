#!/bin/bash

# pip install --upgrade pip
# pip install -r /app/requirements.txt -v

/usr/local/bin/python3 /app/database_init.py

gunicorn 'app:api' -c /app/conf/gunicorn_conf.py --reload