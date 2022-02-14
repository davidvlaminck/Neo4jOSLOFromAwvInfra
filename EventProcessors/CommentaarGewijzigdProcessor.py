import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class CommentaarGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        logging.info(f'started changing notitie of {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            korte_uri = asset_dict['typeURI'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]
            self.tx_context.run(f"MATCH (a:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a.isActief = $isActief",
                                uuid=asset_dict['assetId.identificator'][0:36],
                                notitie=asset_dict['AIMObject.notitie'])
        logging.info('done')
