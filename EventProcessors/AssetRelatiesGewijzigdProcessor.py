import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError, AssetRelationNotCreatedError
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class AssetRelatiesGewijzigdProcessor(SpecificEventProcessor, RelatieProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetrelatie_dicts = self.emInfraImporter.import_assetrelaties_from_webservice_by_assetuuids(asset_uuids=uuids)

        self.process_dicts(assetrelatie_dicts, uuids)

    def process_dicts(self, assetrelatie_dicts, uuids: [str]):
        logging.info(f'started creating {len(assetrelatie_dicts)} assetrelaties')
        self.remove_all_asset_relaties(uuids)
        for assetrelatie_dict in assetrelatie_dicts:
            try:
                self.create_assetrelatie_from_jsonLd_dict(assetrelatie_dict)
            except RelationNotCreatedError as ex:
                raise AssetRelationNotCreatedError(str(ex))

        logging.info('done')
