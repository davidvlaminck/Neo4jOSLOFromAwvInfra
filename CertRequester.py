import os
from pathlib import Path

from requests import Response

from AbstractRequester import AbstractRequester


class CertRequester(AbstractRequester):
    def __init__(self, cert_path: Path, key_path: Path, first_part_url: str = ''):
        super().__init__(first_part_url=first_part_url)
        self.cert_path = cert_path
        self.key_path = key_path

        if not os.path.isfile(cert_path):
            raise FileNotFoundError(f"{cert_path} is not a valid path. Cert file does not exist.")
        if not os.path.isfile(key_path):
            raise FileNotFoundError(f"{key_path} is not a valid path. Key file does not exist.")

    def get(self, url: str = '', **kwargs) -> Response:
        return super().get(url=url, cert=(str(self.cert_path), str(self.key_path)), **kwargs)

    def post(self, url: str = '', **kwargs) -> Response:
        return super().post(url=url, cert=(str(self.cert_path), str(self.key_path)), **kwargs)

    def put(self, url: str = '', **kwargs) -> Response:
        return super().put(url=url, cert=(str(self.cert_path), str(self.key_path)), **kwargs)

    def patch(self, url: str = '', **kwargs) -> Response:
        return super().patch(url=url, cert=(str(self.cert_path), str(self.key_path)), **kwargs)

    def delete(self, url: str = '', **kwargs) -> Response:
        return super().delete(url=url, cert=(str(self.cert_path), str(self.key_path)), **kwargs)
