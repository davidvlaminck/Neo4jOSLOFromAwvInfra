import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class GeometrieOrLocatieGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        self.process_dicts(assetDicts)

    def process_dicts(self, assetDicts):
        asset_processor = NieuwAssetProcessor()
        logging.info(f'started changing geometrie/locatie of {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            flattened_dict = asset_processor.flatten_dict(input_dict=asset_dict)

            korte_uri = flattened_dict['typeURI'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]
            if '-' in assettype or '.' in assettype:
                assettype = f'`{assettype}`'

            flattened_dict["geometry"] = asset_processor.get_wkt_from_puntlocatie(flattened_dict)
            if 'loc:geometrie' in flattened_dict.keys():
                geometrie = flattened_dict['loc:geometrie']
                if geometrie != '' and flattened_dict["geometry"] == '':
                    flattened_dict["geometry"] = geometrie

            attributen = ['geometry', 'loc:geometrie', 'loc:omschrijving', 'loc:puntlocatie.loc:adres.loc:bus',
                          'loc:puntlocatie.loc:adres.loc:gemeente', 'loc:puntlocatie.loc:adres.loc:nummer',
                          'loc:puntlocatie.loc:adres.loc:postcode', 'loc:puntlocatie.loc:adres.loc:provincie',
                          'loc:puntlocatie.loc:adres.loc:straat', 'loc:puntlocatie.loc:bron',
                          'loc:puntlocatie.loc:precisie',
                          'loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:xcoordinaat',
                          'loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:ycoordinaat',
                          'loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:zcoordinaat',
                          'loc:puntlocatie.loc:weglocatie.loc:gemeente', 'loc:puntlocatie.loc:weglocatie.loc:ident2',
                          'loc:puntlocatie.loc:weglocatie.loc:ident8',
                          'loc:puntlocatie.loc:weglocatie.loc:referentiepaalAfstand',
                          'loc:puntlocatie.loc:weglocatie.loc:referentiepaalOpschrift',
                          'loc:puntlocatie.loc:weglocatie.loc:straatnaam']

            params = {attribuut: (flattened_dict[attribuut] if attribuut in flattened_dict.keys() else None)
                      for attribuut in attributen}
            self.tx_context.run(f"MATCH (a:Asset:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a += $params",
                                uuid=self.get_uuid_from_asset_dict(asset_dict), params=params)

        logging.info('done')
