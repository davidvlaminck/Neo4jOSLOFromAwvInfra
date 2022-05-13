import json
import os

import requests
from requests import Response


class RequestHandler:
    def __init__(self, requester):
        self.requester = requester

    def get_jsondict(self, url):
        response = self._perform_get_request(url)
        decoded_string = response.content.decode("utf-8")
        dict_obj = json.loads(decoded_string)
        return dict_obj

    def _perform_get_request(self, url) -> Response:
        return self.requester.get(url=url)

    def perform_post_request(self, url, json_data=None, **kwargs) -> Response:
        if json_data is not None:
            kwargs['json'] = json_data
        return self.requester.post(url=url, **kwargs)
