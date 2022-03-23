import json
import logging
import time

from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError, AssetRelationNotCreatedError, \
    BetrokkeneRelationNotCreatedError


class RelatieProcessor:
    def __init__(self):
        self.tx_context = None

    def remove_all_asset_relaties(self, asset_uuids: [str]):
        start = time.time()
        query = f"UNWIND $params as uuids " \
                "MATCH ({uuid: uuids})-[r]-() WHERE r <> 'HeeftBetrokkene' DELETE r"
        self.tx_context.run(query, params=asset_uuids)
        end = time.time()
        logging.info(f'removed_all_asset_relaties_from {len(asset_uuids)} assets in {str(round(end - start, 2))} seconds.')

    def remove_all_betrokkene_relaties(self, asset_uuids: [str]):
        start = time.time()
        query = f"UNWIND $params as uuids " \
                "MATCH ({uuid: uuids})-[r:HeeftBetrokkene]-() DELETE r"
        self.tx_context.run(query, params=asset_uuids)
        end = time.time()
        logging.info(f'removed_all_betrokkene_relaties_from {len(asset_uuids)} assets in {str(round(end - start, 2))} seconds.')

    @staticmethod
    def _create_assetrelatie_by_dict(tx, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        query = "MATCH (a:Asset), (b) " \
                f"WHERE a.uuid = '{bron_uuid}' " \
                f"AND b.uuid = '{doel_uuid}' " \
                f"CREATE (a)-[r:{relatie_type} " \
                "$params]->(b) " \
                f"RETURN r"
        return tx.run(query, params=params).data()

    def create_assetrelatie_from_jsonLd_dict(self, json_dict):
        relatie_dict = {'assetIdUri': json_dict['@id'], 'typeURI': json_dict['@type'],
                        'isActief': json_dict["AIMDBStatus.isActief"],
                        'uuid': json_dict['RelatieObject.assetId']['DtcIdentificator.identificator'][0:36]}

        bron_uuid = json_dict['RelatieObject.bronAssetId']['DtcIdentificator.identificator'][0:36]
        doel_uuid = json_dict['RelatieObject.doelAssetId']['DtcIdentificator.identificator'][0:36]
        relatie_type = json_dict["RelatieObject.typeURI"].split('#')[1]

        for k, v in json_dict.items():
            if k in ['@type', '@id', "RelatieObject.doel", "RelatieObject.assetId", "AIMDBStatus.isActief",
                     "RelatieObject.bronAssetId", "RelatieObject.doelAssetId", "RelatieObject.typeURI", "RelatieObject.bron"]:
                continue
            if isinstance(v, dict):
                relatie_dict[k] = json.dumps(v)
            else:
                relatie_dict[k] = v

        relatie = self._create_assetrelatie_by_dict(tx=self.tx_context, bron_uuid=bron_uuid, doel_uuid=doel_uuid,
                                                    relatie_type=relatie_type,
                                                    params=relatie_dict)
        if len(relatie) == 0:
            raise AssetRelationNotCreatedError('One of the nodes might be missing')

    def create_betrokkenerelatie_from_jsonLd_dict(self, json_dict):
        flattened_dict = NieuwAssetProcessor().flatten_dict(json_dict)

        relatie_dict = {'assetIdUri': json_dict['@id'], 'typeURI': json_dict['@type'],
                        'isActief': json_dict["AIMDBStatus.isActief"],
                        'uuid': json_dict['@id'].split('/')[-1][0:36]}

        bron_uuid = json_dict['RelatieObject.bron']['@id'].split('/')[-1][0:36]
        doel_uuid = json_dict['RelatieObject.doel']['@id'].split('/')[-1][0:36]
        relatie_type = json_dict["@type"].split('#')[1]

        for k, v in flattened_dict.items():
            if k in ['@type', '@id', "RelatieObject.bron.@type", "RelatieObject.bron.@id", "RelatieObject.doel.@type",
                     "RelatieObject.doel.@id", "AIMDBStatus.isActief"]:
                continue
            if k == 'HeeftBetrokkene.rol':
                relatie_dict[k] = v.replace('https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetrokkenheidRol/', '')
            else:
                relatie_dict[k] = v

        relatie = self._create_assetrelatie_by_dict(tx=self.tx_context, bron_uuid=bron_uuid, doel_uuid=doel_uuid,
                                                    relatie_type=relatie_type,
                                                    params=relatie_dict)
        if len(relatie) == 0:
            raise BetrokkeneRelationNotCreatedError('One of the nodes might be missing')
