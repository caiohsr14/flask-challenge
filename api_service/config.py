"""Default configuration

Use env var to override
"""
import os


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/api_service/api_service.sqlite3"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////app/api_service/api_service.sqlite3"


STOCK_URL = os.getenv("STOCK_URL")
