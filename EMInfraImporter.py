import base64
import json

from RequestHandler import RequestHandler


class EMInfraImporter:
    def __init__(self, request_handler: RequestHandler):
        self.request_handler = request_handler
        self.request_handler.requester.first_part_url += 'eminfra/'
        self.cursor = ''

    def get_events_from_page(self, page_num: int, page_size: int = 1):
        url = f"feedproxy/feed/assets/{page_num}/{page_size}"
        return self.request_handler.get_jsondict(url)

    def get_objects_from_oslo_search_endpoint(self, url_part: str, filter_string: str = '{}', size: int = 100,
                                              only_next_page: bool = False) -> [dict]:
        url = f"core/api/otl/{url_part}/search"
        body_fixed_part = '{"size": ' + f'{size}' + ''
        if filter_string != '{}':
            body_fixed_part += ', "filters": ' + filter_string

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
            if only_next_page:
                return json_list
            if self.cursor == '':
                return json_list

    def get_assets_from_webservice_by_naam(self, naam: str) -> [dict]:
        filter_string = '{ "naam": ' + f'"{naam}"' + ' }'
        return self.get_objects_from_oslo_search_endpoint(url_part='assets', filter_string=filter_string)

    def import_all_assets_from_webservice(self) -> [dict]:
        return self.get_objects_from_oslo_search_endpoint(url_part='assets')

    def import_assets_from_webservice_page_by_page(self, page_size: int) -> [dict]:
        return self.get_objects_from_oslo_search_endpoint(url_part='assets', size=page_size, only_next_page=True)

    def import_assets_from_webservice_by_uuids(self, asset_uuids: [str]) -> [dict]:
        asset_list_string = '", "'.join(asset_uuids)
        filter_string = '{ "uuid": ' + f'["{asset_list_string}"]' + ' }'
        return self.get_objects_from_oslo_search_endpoint(url_part='assets', filter_string=filter_string)

    def import_all_agents_from_webservice(self) -> [dict]:
        return self.get_objects_from_oslo_search_endpoint(url_part='agents')

    def import_agents_from_webservice_page_by_page(self, page_size: int) -> [dict]:
        return self.get_objects_from_oslo_search_endpoint(url_part='agents', size=page_size, only_next_page=True)

    def import_agents_from_webservice_by_uuids(self, agent_uuids: [str]) -> [dict]:
        agent_list_string = '", "'.join(agent_uuids)
        filter_string = '{ "uuid": ' + f'["{agent_list_string}"]' + ' }'
        return self.get_objects_from_oslo_search_endpoint(url_part='agents', filter_string=filter_string)

    def import_all_assetrelaties_from_webservice(self) -> [dict]:
        return self.get_distinct_set_from_list_of_relations(
            self.get_objects_from_oslo_search_endpoint(url_part='assetrelaties'))

    def import_assetrelaties_from_webservice_page_by_page(self, page_size: int) -> [dict]:
        return self.get_distinct_set_from_list_of_relations(
            self.get_objects_from_oslo_search_endpoint(url_part='assetrelaties', size=page_size, only_next_page=True))

    def import_assetrelaties_from_webservice_by_assetuuids(self, asset_uuids: [str]) -> [dict]:
        asset_list_string = '", "'.join(asset_uuids)
        filter_string = '{ "asset": ' + f'["{asset_list_string}"]' + ' }'
        return self.get_distinct_set_from_list_of_relations(
            self.get_objects_from_oslo_search_endpoint(url_part='assetrelaties', filter_string=filter_string))

    def import_all_betrokkenerelaties_from_webservice(self) -> [dict]:
        return self.get_distinct_set_from_list_of_relations(
            self.get_objects_from_oslo_search_endpoint(url_part='betrokkenerelaties'))

    def import_betrokkenerelaties_from_webservice_page_by_page(self, page_size: int) -> [dict]:
        return self.get_distinct_set_from_list_of_relations(
            self.get_objects_from_oslo_search_endpoint(url_part='betrokkenerelaties', size=page_size, only_next_page=True))

    def import_betrokkenerelaties_from_webservice_by_assetuuids(self, asset_uuids: [str]) -> [dict]:
        asset_list_string = '", "'.join(asset_uuids)
        filter_string = '{ "bronAsset": ' + f'["{asset_list_string}"]' + ' }'
        return self.get_distinct_set_from_list_of_relations(
            self.get_objects_from_oslo_search_endpoint(url_part='betrokkenerelaties', filter_string=filter_string))

    @staticmethod
    def get_asset_id_from_uuid_and_typeURI(uuid, typeURI):
        shortUri = typeURI.split('/ns/')[1]
        shortUri_encoded = base64.b64encode(shortUri.encode('utf-8'))
        return uuid + '-' + shortUri_encoded.decode("utf-8")

    @staticmethod
    def get_distinct_set_from_list_of_relations(relation_list: [dict]) -> [dict]:
        return list({x["@id"]: x for x in relation_list}.values())

