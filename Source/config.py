import os


import sys
sys.dont_write_bytecode = True

class Config:
    SECRET_KEY = 'tassaract'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/bookit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


