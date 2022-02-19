import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError, BetrokkeneRelationNotCreatedError
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class BetrokkeneRelatiesGewijzigdProcessor(SpecificEventProcessor, RelatieProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        betrokkenerelatie_dicts = self.emInfraImporter.import_betrokkenerelaties_from_webservice_by_assetuuids(
            asset_uuids=uuids)

        self.process_dicts(betrokkenerelatie_dicts, uuids)

    def process_dicts(self, betrokkenerelatie_dicts, uuids):
        logging.info(f'started creating {len(betrokkenerelatie_dicts)} betrokkenerelaties')
        self.remove_all_betrokkene_relaties(uuids)
        for betrokkenerelatie_dict in betrokkenerelatie_dicts:
            try:
                self.create_betrokkenerelatie_from_jsonLd_dict(betrokkenerelatie_dict)
            except RelationNotCreatedError as ex:
                raise BetrokkeneRelationNotCreatedError(str(ex))
        logging.info('done')
