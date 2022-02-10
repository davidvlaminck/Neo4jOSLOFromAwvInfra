import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class NieuweInstallatieProcessor(SpecificEventProcessor, NieuwAssetProcessor, RelatieProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str], full_sync: bool = False):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        logging.info(f'started creating {len(assetDicts)} assets')
        for assetdict in assetDicts:
            self.create_asset_from_jsonLd_dict(assetdict)
        logging.info('done')

        if full_sync:
            self.remove_all_asset_relaties(uuids)
            assetrelatieDicts = self.emInfraImporter.import_assetrelaties_from_webservice_by_assetuuids(asset_uuids=uuids)
            logging.info(f'started creating {len(assetrelatieDicts)} relations')
            for assetrelatieDict in assetrelatieDicts:
                self.create_assetrelatie_from_jsonLd_dict(assetrelatieDict)
            logging.info('done')
