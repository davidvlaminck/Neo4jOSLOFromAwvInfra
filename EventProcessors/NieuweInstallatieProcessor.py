from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from SpecificEventProcessor import SpecificEventProcessor


class NieuweInstallatieProcessor(SpecificEventProcessor, NieuwAssetProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        # get asset dict jsonld from importer
        # process result dict one by one in loop
        self.create_asset_by_dict()
