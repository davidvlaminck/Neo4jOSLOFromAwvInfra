import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class SchadebeheerderGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)
        asset_processor = NieuwAssetProcessor()

        logging.info(f'started changing schadebeheerder of {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            korte_uri = asset_dict['typeURI'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]

            flattened_dict = asset_processor.flatten_dict(input_dict=asset_dict)

            toezicht_attributen = ['tz:schadebeheerder.tz:naam', 'tz:schadebeheerder.tz:referentie']

            params = {}
            for attribuut in toezicht_attributen:
                if attribuut in flattened_dict.keys():
                    params[attribuut] = flattened_dict[attribuut]
                else:
                    params[attribuut] = None

            self.tx_context.run(f"MATCH (a:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a += :params",
                                uuid=asset_dict['assetId.identificator'][0:36],
                                params=params)
        logging.info('done')
