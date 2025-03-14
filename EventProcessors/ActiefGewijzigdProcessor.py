import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class ActiefGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        self.process_dicts(assetDicts)

    def process_dicts(self, assetDicts):
        logging.info(f'started changing actief of {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            korte_uri = asset_dict['@type'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]
            if '-' in assettype or '.' in assettype:
                assettype = f'`{assettype}`'
            self.tx_context.run(f"MATCH (a:Asset:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a.isActief = $isActief",
                                uuid=self.get_uuid_from_asset_dict(asset_dict),
                                isActief=asset_dict.get('AIMDBStatus.isActief', True))
        logging.info('done')
