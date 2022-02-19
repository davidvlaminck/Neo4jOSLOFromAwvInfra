import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class NieuweInstallatieProcessor(SpecificEventProcessor, NieuwAssetProcessor, RelatieProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str], full_sync: bool = False):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        logging.info(f'started creating {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            self.create_asset_from_jsonLd_dict(asset_dict)

        if full_sync:
            self.remove_all_asset_relaties(uuids)
            self.remove_all_betrokkene_relaties(uuids)
            assetrelatie_dicts = self.emInfraImporter.import_assetrelaties_from_webservice_by_assetuuids(asset_uuids=uuids)
            betrokkenerelatie_dicts = self.emInfraImporter.import_betrokkenerelaties_from_webservice_by_assetuuids(
                asset_uuids=uuids)
            logging.info(f'started creating {len(assetrelatie_dicts) + len(betrokkenerelatie_dicts)} relations')
            for assetrelatieDict in assetrelatie_dicts:
                try:
                    self.create_assetrelatie_from_jsonLd_dict(assetrelatieDict)
                except RelationNotCreatedError as ex:
                    pass  # fix for creating relationships between assets where one of the nodes does not exist yet
            for betrokkenerelatieDict in betrokkenerelatie_dicts:
                self.create_betrokkenerelatie_from_jsonLd_dict(betrokkenerelatieDict)

        logging.info('done')
