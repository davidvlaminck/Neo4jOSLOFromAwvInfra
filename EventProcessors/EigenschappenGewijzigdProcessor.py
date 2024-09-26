import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class EigenschappenGewijzigdProcessor(SpecificEventProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        asset_dicts = self.emInfraImporter.import_assets_from_webservice_by_uuids(asset_uuids=uuids)

        self.process_dicts(asset_dicts)

    def process_dicts(self, asset_dicts):
        asset_processor = NieuwAssetProcessor()
        logging.info(f'started changing eigenschappen of {len(asset_dicts)} assets')

        excluded_attributes = ['@type', '@id', 'assetIdUri', 'assetId.identificator', 'assetId.toegekendDoor',
                               'isActief', 'uuid',
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
                               'loc:puntlocatie.loc:weglocatie.loc:gemeente',
                               'loc:puntlocatie.loc:weglocatie.loc:ident2',
                               'loc:puntlocatie.loc:weglocatie.loc:ident8',
                               'loc:puntlocatie.loc:weglocatie.loc:referentiepaalAfstand',
                               'loc:puntlocatie.loc:weglocatie.loc:referentiepaalOpschrift',
                               'loc:puntlocatie.loc:weglocatie.loc:straatnaam',
                               'wl:Weglocatie.wegaanduiding', 'wl:Weglocatie.geometrie', 'wl:Weglocatie.wegsegment',
                               'wl:Weglocatie.bron', 'wl:Weglocatie.score', 'bs:Bestek.bestekkoppeling']

        # for all assets remove the non-excluded-properties
        properties_keep_str = ('{.' + ', .'.join([f'`{a}`' if '-' in a or '@' in a or '.' in a or ':' in a else a
                                                  for a in excluded_attributes])) + '}'
        uuids_str = "['" + "','".join([a['@id'][39:75] for a in asset_dicts]) + "']"

        self.tx_context.run(f"""MATCH (n:Asset) 
                                WHERE n.uuid in {uuids_str} 
                                WITH n, n {properties_keep_str} as propsToKeep 
                                SET n = propsToKeep""")

        for asset_dict in asset_dicts:
            flattened_dict = asset_processor.flatten_dict(input_dict=asset_dict)

            korte_uri = flattened_dict['typeURI'].split('/ns/')[1]
            ns = korte_uri.split('#')[0]
            assettype = korte_uri.split('#')[1]
            if '-' in assettype or '.' in assettype:
                assettype = f'`{assettype}`'

            params = {attribuut: flattened_dict[attribuut] for attribuut in flattened_dict.keys()
                      if attribuut not in excluded_attributes}
            self.tx_context.run(f"MATCH (a:Asset:{ns}:{assettype} "
                                "{uuid: $uuid}) SET a += $params",
                                uuid=self.get_uuid_from_asset_dict(asset_dict),
                                params=params)
        logging.info('done')
