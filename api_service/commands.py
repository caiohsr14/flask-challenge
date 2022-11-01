# encoding: utf-8

import click
from flask import Blueprint
from flask.cli import with_appcontext

blueprint = Blueprint("admin", __name__)

@blueprint.cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from api_service.extensions import db
    from api_service.models import User

    click.echo("create admin user")
    user = User(username="admin", email="admin@mail.com", password="admin", active=True, role='ADMIN')
    db.session.add(user)
    user = User(username="johndoe", email="johndoe@mail.com", password="john", active=True, role='USER')
    db.session.add(user)
    db.session.commit()
    click.echo("created users.")
