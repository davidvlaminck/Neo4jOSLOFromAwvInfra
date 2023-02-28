import datetime
import json
import sys
from pathlib import Path

import jwt  # pip install pyjwt and cryptography
import jwt.algorithms as jwt_algo
import requests
import string

from random import choice

from requests import Response


class JWTRequester(requests.Session):
    def __init__(self, private_key_path: Path, client_id: str, first_part_url: str = ''):
        if 'cryptography' not in sys.modules:
            raise ModuleNotFoundError('needs module cryptography to work')

        self.private_key_path: Path = private_key_path
        self.client_id: str = client_id
        self.first_part_url: str = first_part_url

        self.oauth_token: str = ''
        self.expires: datetime.datetime = datetime.datetime.now() - datetime.timedelta(seconds=1)
        self.requested_at: datetime.datetime = self.expires
        super().__init__()

    def get(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().get(url=self.first_part_url + url, **kwargs)

    def post(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().post(url=self.first_part_url + url, **kwargs)

    def put(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().put(url=self.first_part_url + url, **kwargs)

    def patch(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().patch(url=self.first_part_url + url, **kwargs)

    def delete(self, url='', **kwargs) -> Response:
        kwargs = self.modify_kwargs_for_bearer_token(kwargs)
        return super().delete(url=self.first_part_url + url, **kwargs)

    def get_oauth_token(self) -> str:
        if self.expires > datetime.datetime.now():
            return self.oauth_token

        authentication_token = self.generate_authentication_token()
        self.oauth_token, expires_in = self.get_access_token(authentication_token)
        self.expires = self.requested_at + datetime.timedelta(seconds=expires_in) - datetime.timedelta(minutes=1)

        return self.oauth_token

    def modify_kwargs_for_bearer_token(self, kwargs: dict) -> dict:
        bearer_token = self.get_oauth_token()
        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        for arg in kwargs:
            if arg == 'headers':
                headers = kwargs[arg]
                if 'accept' not in headers:
                    headers['accept'] = ''
                if headers['accept'] is not None:
                    if headers['accept'] != '':
                        headers['accept'] = f"{headers['accept']}, application/json"
                    else:
                        headers['accept'] = 'application/json'
                headers['authorization'] = f'Bearer {bearer_token}'
                if 'Content-Type' not in headers or headers['Content-Type'] is None:
                    headers['Content-Type'] = 'application/vnd.awv.eminfra.v1+json'
                kwargs['headers'] = headers

        return kwargs

    def generate_authentication_token(self) -> str:
        self.requested_at = datetime.datetime.utcnow()
        # Authentication token generation
        payload = {'iss': self.client_id,
                   'sub': self.client_id,
                   'aud': 'https://authenticatie.vlaanderen.be/op',
                   'exp': self.requested_at + datetime.timedelta(minutes=9),
                   'jti': ''.join(choice(string.ascii_lowercase) for _ in range(20))
                   }

        with open(self.private_key_path) as private_key:
            private_key_json = json.load(private_key)
            key = jwt_algo.RSAAlgorithm.from_jwk(private_key_json)
            token = jwt.encode(payload=payload, key=key, algorithm='RS256')

        return token

    def get_access_token(self, token: str) -> (str, int):
        # Authorization access token generation
        url = 'https://authenticatie.vlaanderen.be/op/v1/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        request_body = {
            'grant_type': 'client_credentials',
            'scope': 'awv_toep_services',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_id': self.client_id,
            "client_assertion": token
        }

        response = requests.post(url, data=request_body, headers=headers)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
            raise RuntimeError(f'Could not get the acces token: {response.content}')

        response_json = response.json()

        return response_json['access_token'], response_json['expires_in']


class SingletonJWTRequester(JWTRequester):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingletonJWTRequester, cls).__new__(cls)
        return cls.instance

