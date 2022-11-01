from api_service.clients.stock import StockObject


def test_stock_query_resource_get(test_client, mocker):
    fake_stock_data = StockObject(
        {
            "high": None,
            "low": None,
            "open": None,
            "close": None,
            "name": "APPL.US",
            "date": None,
            "time": None,
            "symbol": "APPL.US",
        }
    )

    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )
    mock_stock_client.get_stock.return_value = fake_stock_data

    expected_result = {"company_name": "APPL.US", "symbol": "APPL.US", "quote": None}

    response = test_client.get("/api/v1/stock?q=test")
    assert response.get_json() == expected_result
    assert response.status_code == 200
    mock_stock_client.get_stock.assert_called_once_with("test")


def test_stock_query_resource_invalid_get(test_client, mocker):
    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )

    response = test_client.get("/api/v1/stock")
    assert b"Missing data for required field" in response.data
    assert response.status_code == 400
    mock_stock_client.get_stock.assert_not_called()


def test_stock_query_resource_get_with_invalid_stock(test_client, mocker):
    mock_stock_client = mocker.patch(
        "api_service.api.resources.StockQuery.stock_client"
    )
    mock_stock_client.get_stock.return_value = None

    response = test_client.get("/api/v1/stock?q=test")
    assert b"Stock not found" in response.data
    assert response.status_code == 404
    mock_stock_client.get_stock.assert_called_once_with("test")
