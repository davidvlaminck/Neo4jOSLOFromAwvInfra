import requests

from AbstractRequester import AbstractRequester
from CertRequester import CertRequester
from Enums import Environment, AuthType
from JWTRequester import JWTRequester


class RequesterFactory:
    first_part_url_dict = {
        Environment.PRD: 'https://services.apps.mow.vlaanderen.be/',
        Environment.TEI: 'https://services.apps-tei.mow.vlaanderen.be/',
        Environment.DEV: 'https://services.apps-dev.mow.vlaanderen.be/',
        Environment.AIM: 'https://services-aim.apps-dev.mow.vlaanderen.be/'
    }

    @classmethod
    def create_requester(cls, auth_type: AuthType, env: Environment, settings: dict = None, **kwargs
                         ) -> AbstractRequester:
        specific_settings = {}
        try:
            if auth_type == AuthType.JWT:
                specific_settings = settings['authentication'][auth_type.name][env.name.lower()]
            elif auth_type == AuthType.CERT:
                specific_settings = settings['authentication'][auth_type.value][env.name.lower()]
        except KeyError as e:
            raise ValueError(f"Could not load the settings for {auth_type} {env}") from e

        try:
            first_part_url = cls.first_part_url_dict[env]
        except KeyError as exc:
            raise ValueError(f"Invalid environment: {env}") from exc

        if auth_type == AuthType.JWT:
            return JWTRequester(private_key_path=specific_settings['key_path'],
                                client_id=specific_settings['client_id'],
                                first_part_url=first_part_url)
        elif auth_type == AuthType.CERT:
            return CertRequester(cert_path=specific_settings['cert_path'],
                                 key_path=specific_settings['key_path'],
                                 first_part_url=first_part_url)
        else:
            raise ValueError(f"Invalid authentication type: {auth_type}")
