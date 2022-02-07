import base64
import json

import requests


class EMInfraImporter:
    def __init__(self, cert_path='', key_path=''):
        self.cert_path = cert_path
        self.key_path = key_path

    def import_assets_from_webservice_by_uuids(self, asset_uuids: [str]):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assets/search"
        asset_list_string = '", "'.join(asset_uuids)
        body = '{"filters": { "uuid": ' + f'["{asset_list_string}"]' + ' }}'
        json_data = json.loads(body)
        response = requests.post(url, cert=(self.cert_path, self.key_path), json=json_data)

        data = response.content.decode("utf-8")
        jsonobj = json.loads(data)
        json_list = jsonobj["@graph"]

        return json_list

    def import_assetrelaties_from_webservice_by_assetuuids(self, asset_uuids: [str]):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assetrelaties/search"
        asset_list_string = '", "'.join(asset_uuids)
        body = '{"filters": { "asset": ' + f'["{asset_list_string}"]' + ' }}'
        json_data = json.loads(body)
        response = requests.post(url, cert=(self.cert_path, self.key_path), json=json_data)

        data = response.content.decode("utf-8")
        jsonobj = json.loads(data)
        json_list = jsonobj["@graph"]

        return json_list

    def import_assetrelaties_from_webservice_by_assetuuid(self, asset_uuid: str):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assetrelaties/search"
        body = '{"filters": { "asset": ' + f'["{asset_uuid}"]' + ' }}'
        json_data = json.loads(body)
        response = requests.post(url, cert=(self.cert_path, self.key_path), json=json_data)

        data = response.content.decode("utf-8")
        jsonobj = json.loads(data)
        json_list = jsonobj["@graph"]

        return json_list

    def import_asset_from_webservice_by_uuid(self, asset_uuid: str):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assets/search"
        body = '{"filters": { "uuid": ' + f'["{asset_uuid}"]' + ' }}'
        json_data = json.loads(body)
        response = requests.post(url, cert=(self.cert_path, self.key_path), json=json_data)

        data = response.content.decode("utf-8")
        jsonobj = json.loads(data)
        json_list = jsonobj["@graph"]

        return json_list

    def import_asset_from_webservice_by_asset_id(self, asset_id):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assets/{asset_id}"
        response = requests.get(url, cert=(self.cert_path, self.key_path))
        data = response.content.decode("utf-8")
        jsonobj = json.loads(data)
        json_list = [jsonobj]

    def import_asset_from_webservice_by_uuid_and_typeURI(self, uuid, typeURI):
        return self.import_asset_from_webservice_by_asset_id(
            self.get_asset_id_from_uuid_and_typeURI(uuid, typeURI)
        )

    @staticmethod
    def get_asset_id_from_uuid_and_typeURI(uuid, typeURI):
        shortUri = typeURI.split('/ns/')[1]
        shortUri_encoded = base64.b64encode(shortUri.encode('utf-8'))
        return uuid + '-' + shortUri_encoded.decode("utf-8")
