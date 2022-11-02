# encoding: utf-8

import os

from api_service import api, commands
from api_service.extensions import db, jwt, migrate
from flask import Flask


def create_app(testing=False):
    app = Flask("api_service")

    if testing:
        app.config.from_object("api_service.config.TestingConfig")
    else:
        env = os.environ.get("FLASK_ENV")
        app.config.from_object("api_service.config.{}Config".format(env))

    app.config.from_prefixed_env()

    configure_extensions(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(commands.blueprint)
