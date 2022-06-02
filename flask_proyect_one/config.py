import os

class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI =  'postgresql://postgres:cargamos2022@localhost:5432/postgres'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://ceclgmqzlavpqc:baab8274e8c1580c3ff2a90fccd9a910d253787a5215c49a93020a649a5ebb62@ec2-54-243-92-68.compute-1.amazonaws.com:5432/dcdt71u55gqvs2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False