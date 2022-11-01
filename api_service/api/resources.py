from api_service.api.schemas import StockInfoSchema, StockQuerySchema
from api_service.clients.stock import StockClient
from api_service.config import STOCK_URL
from api_service.extensions import db
from flask import abort, request
from flask_restful import Resource


class StockQuery(Resource):
    """
    Endpoint to allow users to query stocks
    """

    stock_client = StockClient(STOCK_URL)

    def get(self):
        query_schema = StockQuerySchema()
        errors = query_schema.validate(request.args)
        if errors:
            abort(400, str(errors))

        stock_data = self.stock_client.get_stock(request.args["q"])
        if not stock_data:
            abort(404, "Stock not found")

        schema = StockInfoSchema()
        return schema.dump(stock_data)


class History(Resource):
    """
    Returns queries made by current user.
    """

    def get(self):
        # TODO: Implement this method.
        pass


class Stats(Resource):
    """
    Allows admin users to see which are the most queried stocks.
    """

    def get(self):
        # TODO: Implement this method.
        pass
