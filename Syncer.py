import json
import os

import requests

from Neo4JConnector import Neo4JConnector


class RequestHandler:
    def __init__(self, cert_path: str, key_path: str):
        if not os.path.isfile(cert_path):
            raise FileNotFoundError('certificate file not found')
        if not os.path.isfile(key_path):
            raise FileNotFoundError('key file not found')
        self.cert_path = cert_path
        self.key_path = key_path

    def perform_get_request(self, url):
        return requests.get(url, cert=(self.cert_path, self.key_path), headers={"accept": "application/vnd.awv.eminfra.v2+json"})

    def get_feedproxy_page(self, page_num):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/feedproxy/feed/assets/{page_num}/1"
        response = self.perform_get_request(url)
        decoded_string = response.content.decode("utf-8")
        dict_obj = json.loads(decoded_string)
        return dict_obj


class Syncer:
    def __init__(self, connector: Neo4JConnector, request_handler: RequestHandler):
        self.connector = connector
        self.request_handler = request_handler


if __name__ == '__main__':
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    request_handler = RequestHandler(cert_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                                     key_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.key')
    syncer = Syncer(connector=connector, request_handler=request_handler)
    page = syncer.get_feedproxy_page(525000)
    pass
