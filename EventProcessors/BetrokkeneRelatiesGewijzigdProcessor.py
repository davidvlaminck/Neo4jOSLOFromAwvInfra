import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class BetrokkeneRelatiesGewijzigdProcessor(SpecificEventProcessor, RelatieProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        betrokkenerelatie_dicts = self.emInfraImporter.import_betrokkenerelaties_from_webservice_by_assetuuids(
            asset_uuids=uuids)

        logging.info(f'started creating {len(betrokkenerelatie_dicts)} betrokkenerelaties')

        self.remove_all_betrokkene_relaties(uuids)
        for betrokkenerelatie_dict in betrokkenerelatie_dicts:
            self.create_betrokkenerelatie_from_jsonLd_dict(betrokkenerelatie_dict)

        logging.info('done')
