# coding: utf-8

import os

DEBUG = True

SECRET_KEY = os.urandom(24)

DB_USER = 'root'
DB_PASSWORD = 'your_db_password'
DB_NAME = 'property'

SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost/{}'.format(DB_USER, DB_PASSWORD, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
