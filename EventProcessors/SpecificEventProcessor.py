from abc import ABC, abstractmethod

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter


class SpecificEventProcessor(ABC):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        self.tx_context = tx_context
        self.emInfraImporter = emInfraImporter

    @abstractmethod
    def process(self, uuids: [str]):
        pass

    @staticmethod
    def get_uuid_from_asset_dict(asset_dict: dict) -> str:
        index = asset_dict['@id'].rfind('/')
        return asset_dict['@id'][index+1:index+37]
