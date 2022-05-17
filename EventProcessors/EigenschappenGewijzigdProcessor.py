import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class EigenschappenGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetDicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        self.process_dicts(assetDicts)

    def process_dicts(self, assetDicts):
        asset_processor = NieuwAssetProcessor()
        logging.info(f'started changing eigenschappen of {len(assetDicts)} assets')
        for asset_dict in assetDicts:
            flattened_dict = asset_processor.flatten_dict(input_dict=asset_dict)

            korte_uri = flattened_dict['typeURI'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]
            if '-' in assettype:
                assettype = '`' + assettype + '`'

            excluded_attributes = ['@type', '@id', 'assetIdUri', 'assetId.identificator', 'assetId.toegekendDoor', 'isActief',
                                   'notitie', 'naam', 'naampad', 'tz:schadebeheerder.tz:naam', 'typeURI',
                                   'tz:schadebeheerder.tz:referentie', 'toestand', 'tz:toezichter.tz:gebruikersnaam',
                                   'tz:toezichter.tz:voornaam', 'tz:toezichter.tz:email',
                                   'tz:toezichter.tz:naam', 'tz:toezichtgroep.tz:naam', 'tz:toezichtgroep.tz:referentie',
                                   'geometry', 'loc:geometrie', 'loc:omschrijving', 'loc:puntlocatie.loc:adres.loc:bus',
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

            params = {}
            for attribuut in flattened_dict.keys():
                if attribuut not in excluded_attributes:
                    params[attribuut] = flattened_dict[attribuut]

            self.tx_context.run(f"MATCH (a:Asset:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a += $params",
                                uuid=flattened_dict['assetId.identificator'][0:36],
                                params=params)
        logging.info('done')
