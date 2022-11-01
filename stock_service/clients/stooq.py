import csv

import requests


class StooqClient(object):
    resource_path = "q/l"

    def __init__(self, base_url):
        self.base_url = base_url

    def get_stock(self, code):
        params = {"s": code, "f": "sd2t2ohlcvn", "e": "csv", "h": ""}
        with requests.get(
            "{}{}".format(self.base_url, self.resource_path), params=params, stream=True
        ) as response:
            try:
                response.raise_for_status()

                lines = (line.decode("utf-8") for line in response.iter_lines())
                reader = csv.DictReader(lines)
                return next(reader)
            except (requests.exceptions.HTTPError, StopIteration):
                return None
