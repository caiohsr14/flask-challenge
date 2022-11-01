import pytest
import requests
import responses
from stock_service.clients.stooq import StooqClient


@pytest.fixture
def client():
    return StooqClient("https://example.com/")


@responses.activate
def test_get_stock(client):
    fake_code = "appl.us"
    fake_response = "Symbol,Date,Time,Open,High,Low,Close,Volume,Name\nAPPL.US,N/D,N/D,N/D,N/D,N/D,N/D,N/D,APPL.US"
    expected_url = "{}{}".format(client.base_url, client.resource_path)

    responses.add(
        responses.GET, expected_url, body=fake_response, status=requests.codes.ok
    )

    expected_data = {
        "Symbol": "APPL.US",
        "Date": "N/D",
        "Time": "N/D",
        "Open": "N/D",
        "High": "N/D",
        "Low": "N/D",
        "Close": "N/D",
        "Volume": "N/D",
        "Name": "APPL.US",
    }
    result = client.get_stock(fake_code)
    assert result == expected_data


@responses.activate
def test_get_stock_with_broken_data(client):
    fake_code = "appl.us"
    fake_response = "broken_data"
    expected_url = "{}{}".format(client.base_url, client.resource_path)

    responses.add(
        responses.GET, expected_url, body=fake_response, status=requests.codes.ok
    )

    result = client.get_stock(fake_code)
    assert result is None


@responses.activate
def test_get_stock_with_error(client):
    fake_code = "appl.us"
    fake_response = "Symbol,Date,Time,Open,High,Low,Close,Volume,Name\nAPPL.US,N/D,N/D,N/D,N/D,N/D,N/D,N/D,APPL.US"
    expected_url = "{}{}".format(client.base_url, client.resource_path)

    responses.add(
        responses.GET,
        expected_url,
        body=fake_response,
        status=requests.codes.bad_request,
    )

    result = client.get_stock(fake_code)
    assert result is None
