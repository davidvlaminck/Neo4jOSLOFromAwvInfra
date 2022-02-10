import json
import os

import requests
from requests import Response


class RequestHandler:
    def __init__(self, cert_path: str, key_path: str, base_path: str = 'https://services.apps.mow.vlaanderen.be/eminfra/'):
        if not os.path.isfile(cert_path):
            raise FileNotFoundError('certificate file not found')
        if not os.path.isfile(key_path):
            raise FileNotFoundError('key file not found')
        self.cert_path = cert_path
        self.key_path = key_path
        self.base_path = base_path

    def get_jsondict(self, url):
        response = self._perform_get_request(url)
        decoded_string = response.content.decode("utf-8")
        dict_obj = json.loads(decoded_string)
        return dict_obj

    def _perform_get_request(self, url) -> Response:
        return requests.get(f'{self.base_path}{url}', cert=(self.cert_path, self.key_path),
                            headers={"accept": "application/vnd.awv.eminfra.v2+json"})

    def perform_post_request(self, url, json_data=None) -> Response:
        return requests.post(f'{self.base_path}{url}', cert=(self.cert_path, self.key_path),
                            headers={"accept": "application/vnd.awv.eminfra.v2+json"}, json=json_data)
