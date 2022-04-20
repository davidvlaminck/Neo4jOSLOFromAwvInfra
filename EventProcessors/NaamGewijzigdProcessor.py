import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class NaamGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        self.process_dicts(assetDicts)

    def process_dicts(self, assetDicts):
        logging.info(f'started changing naam/naampad of {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            korte_uri = asset_dict['@type'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]
            naampad = None
            naam = None
            if 'NaampadObject.naampad' in asset_dict:
                naampad = asset_dict['NaampadObject.naampad']
            if 'AIMNaamObject.naam' in asset_dict:
                naam = asset_dict['AIMNaamObject.naam']
            self.tx_context.run(f"MATCH (a:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a.naam = $naam, a.naampad = $naampad",
                                uuid=asset_dict['AIMObject.assetId']['DtcIdentificator.identificator'][0:36],
                                naam=naam,
                                naampad=naampad)
        logging.info('done')
