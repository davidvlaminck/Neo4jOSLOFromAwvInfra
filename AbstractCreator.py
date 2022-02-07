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