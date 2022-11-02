# encoding: utf-8

import json

import pytest
from api_service.app import create_app
from api_service.clients.stock import StockClient
from api_service.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    return app


@pytest.fixture()
def db():
    return _db


@pytest.fixture
def test_client(app):
    return app.test_client()


@pytest.fixture
def stock_client():
    return StockClient("https://example.com/")


def get_login_token(test_client, username, password):
    login_data = {"username": username, "password": password}
    response = test_client.post(
        "/api/v1/login",
        data=json.dumps(login_data),
        headers={"Content-Type": "application/json"},
    )
    json_data = response.get_json()
    return json_data["token"]


@pytest.fixture
def admin_token(test_client):
    return get_login_token(test_client, "admin", "admin")


@pytest.fixture
def user_token(test_client):
    return get_login_token(test_client, "johndoe", "john")
