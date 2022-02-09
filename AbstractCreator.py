import json
from abc import abstractmethod

from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector


class AbstractCreator:
    def __init__(self, neo4JConnector: Neo4JConnector = None, eminfraImporter: EMInfraImporter = None):
        self.connector = neo4JConnector
        self.eminfraImporter = eminfraImporter

    def create_assets_from_eminfra(self, list_uuids: [str]):
        jsonList = self.eminfraImporter.import_assets_from_webservice_by_uuids(list_uuids)
        for jsonDict in jsonList:
            self.create_asset_from_jsonLd_dict(jsonDict)

    def create_relaties_from_eminfra(self, list_uuids: [str]):
        jsonList = self.eminfraImporter.import_assetrelaties_from_webservice_by_assetuuids(list_uuids)
        for jsonDict in jsonList:
            if jsonDict["@id"] == 'https://data.awvvlaanderen.be/id/assetrelatie/2b15f9d7-d308-4411-9ea6-9e0d0d415f03-b25kZXJkZWVsI0hvb3J0Qmlq':
                pass
            self.create_relatie_from_jsonLd_dict(jsonDict)

    def create_assets_from_jsonLD_file(self, filePath):
        with open(filePath, 'r') as file:
            data = file.read()
        jsonList = json.loads(data)
        for jsonDict in jsonList:
            self.create_asset_from_jsonLd_dict(jsonDict)

    @abstractmethod
    def create_asset_from_jsonLd_dict(self, jsonDict):
        pass

    @abstractmethod
    def create_relatie_from_jsonLd_dict(self, jsonDict):
        pass

    def flatten_dict(self, input_dict:dict, seperator:str = '.', prefix='', affix='', new_dict=None):
        if new_dict is None:
            new_dict = {}
        for k, v in input_dict.items():
            if isinstance(v, dict):
                self.flatten_dict(input_dict=v, prefix=k, new_dict=new_dict)
            elif isinstance(v, list):
                for i in range(0, len(v)):
                    if isinstance(v[i], dict):
                        self.flatten_dict(input_dict=v[i], prefix=k, affix='[' + str(i) + ']', new_dict=new_dict)
                    else:
                        if prefix != '':
                            new_dict[prefix + seperator + k + '[' + str(i) + ']'] = v[i]
                        else:
                            new_dict[k + '[' + str(i) + ']'] = v[i]
            else:
                if prefix != '':
                    new_dict[prefix + affix + seperator + k] = v
                else:
                    new_dict[k] = v

        return new_dict