import base64
import json

import requests

from RequestHandler import RequestHandler


class EMInfraImporter:
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler
        self.cursor = ''

    def get_event_from_page(self, page_num: int):
        url = f"feedproxy/feed/assets/{page_num}/1"
        return self.request_handler.get_jsondict(url)

    def get_objects_from_oslo_search_endpoint(self, url_part: str, filter_string: str = '{}', size: int = 100) -> [dict]:
        url = f"core/api/otl/{url_part}/search"
        body_fixed_part = '{"size": ' + f'{size}' + ', "filters": ' + filter_string

        json_list = []
        while True:
            body = body_fixed_part
            if self.cursor != '':
                body += ', "fromCursor": ' + f'"{self.cursor}"'
            body += '}'
            json_data = json.loads(body)

            response = self.request_handler.perform_post_request(url=url, json_data=json_data)

            decoded_string = response.content.decode("utf-8")
            dict_obj = json.loads(decoded_string)
            keys = response.headers.keys()
            json_list.extend(dict_obj['@graph'])
            if 'em-paging-next-cursor' in keys:
                self.cursor = response.headers['em-paging-next-cursor']
            else:
                self.cursor = ''
            if self.cursor == '':
                return json_list

    def import_assets_from_webservice_by_uuids(self, asset_uuids: [str]) -> [dict]:
        asset_list_string = '", "'.join(asset_uuids)
        filter_string = '{ "uuid": ' + f'["{asset_list_string}"]' + ' }'
        return self.get_objects_from_oslo_search_endpoint(url_part='assets', filter_string=filter_string)

    def import_assetrelaties_from_webservice_by_assetuuids(self, asset_uuids: [str]) -> [dict]:
        asset_list_string = '", "'.join(asset_uuids)
        filter_string = '{ "asset": ' + f'["{asset_list_string}"]' + ' }'
        return self.get_objects_from_oslo_search_endpoint(url_part='assetrelaties', filter_string=filter_string)

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
