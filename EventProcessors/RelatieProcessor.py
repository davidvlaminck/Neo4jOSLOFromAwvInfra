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
        query = "UNWIND $params as uuids MATCH (a:Asset {uuid: uuids})-[r]-(b:Asset) DELETE r"
        self.tx_context.run(query, params=asset_uuids)
        end = time.time()
        logging.info(
            f'removed_all_asset_relaties_from {len(asset_uuids)} assets in {str(round(end - start, 2))} seconds.')

    def remove_all_betrokkene_relaties(self, asset_uuids: [str]):
        start = time.time()
        query = "UNWIND $params as uuids MATCH (:Asset {uuid: uuids})-[r:HeeftBetrokkene]-(a:Agent) DELETE r"
        self.tx_context.run(query, params=asset_uuids)
        end = time.time()
        logging.info(
            f'removed_all_betrokkene_relaties_from {len(asset_uuids)} assets in {str(round(end - start, 2))} seconds.')

    @staticmethod
    def _create_relatie_by_dict(tx, bron_uuid: str = '', doel_uuid: str = '', relatie_type: str = '', params=None):
        query = "MATCH (a {uuid: '" + bron_uuid + "'}), (b {uuid: '" + doel_uuid + "'}) " \
                                                                                   f"CREATE (a)-[r:{relatie_type} " \
                                                                                   "$params]->(b) " \
                                                                                   f"RETURN a, r, b"
        return tx.run(query, params=params).data()

    def create_assetrelatie_from_jsonLd_dict(self, json_dict):
        relatie_dict = {'assetIdUri': json_dict['@id'], 'typeURI': json_dict['@type'],
                        'uuid': json_dict['@id'][46:82]}

        if "AIMDBStatus.isActief" in json_dict:
            relatie_dict['isActief'] = json_dict["AIMDBStatus.isActief"]

        bron_uuid = json_dict['RelatieObject.bron']['@id'][39:75]
        doel_uuid = json_dict['RelatieObject.doel']['@id'][39:75]
        relatie_type = json_dict['@type'].split('#')[1]

        for k, v in json_dict.items():
            if k in ['@type', '@id', "RelatieObject.doel", "RelatieObject.assetId", "AIMDBStatus.isActief",
                     "RelatieObject.bronAssetId", "RelatieObject.doelAssetId", "RelatieObject.typeURI",
                     "RelatieObject.bron"]:
                continue
            relatie_dict[k] = json.dumps(v) if isinstance(v, dict) else v
        query = "MATCH (a:Asset {uuid: '" + bron_uuid + "'}), (b:Asset {uuid: '" + doel_uuid + "'}) " \
                                                                                                   f"CREATE (a)-[r:{relatie_type} $params]->(b) " \
                                                                                                   f"RETURN a, r, b"
        relatie = self.tx_context.run(query, params=relatie_dict).data()

        if len(relatie) == 0:
            raise AssetRelationNotCreatedError('One of the nodes might be missing')

    def create_betrokkenerelatie_from_jsonLd_dict(self, json_dict):
        flattened_dict = NieuwAssetProcessor().flatten_dict(json_dict)

        relatie_dict = {
            'assetIdUri': json_dict['@id'],
            'typeURI': json_dict['@type'],
            'isActief': json_dict["AIMDBStatus.isActief"],
            'uuid': json_dict['@id'].split('/')[-1][:36],
        }

        bron_uuid = json_dict['RelatieObject.bron']['@id'].split('/')[-1][:36]
        doel_uuid = json_dict['RelatieObject.doel']['@id'].split('/')[-1][:36]

        for k, v in flattened_dict.items():
            if k in ['@type', '@id', "RelatieObject.bron.@type", "RelatieObject.bron.@id", "RelatieObject.doel.@type",
                     "RelatieObject.doel.@id", "AIMDBStatus.isActief"]:
                continue
            if k == 'HeeftBetrokkene.rol':
                relatie_dict[k] = v.replace('https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetrokkenheidRol/',
                                            '')
            else:
                relatie_dict[k] = v

        if json_dict['RelatieObject.bron']['@type'] == 'http://purl.org/dc/terms/Agent':
            query = (
                "MATCH (a:Agent {uuid: '" + bron_uuid + "'}), (b:Agent {uuid: '" + doel_uuid
                + "'}) CREATE (a)-[r:HeeftBetrokkene $params]->(b) RETURN a, r, b")
        else:
            query = (
                "MATCH (a:Asset {uuid: '" + bron_uuid + "'}), (b:Agent {uuid: '" + doel_uuid
                + "'}) CREATE (a)-[r:HeeftBetrokkene $params]->(b) RETURN a, r, b")
        relatie = self.tx_context.run(query, params=relatie_dict).data()

        if len(relatie) == 0:
            ex = BetrokkeneRelationNotCreatedError(message='One of the nodes might be missing')
            if json_dict['RelatieObject.doel']['@type'] == 'http://purl.org/dc/terms/Agent':
                query = "MATCH (a:Agent {uuid: '" + doel_uuid + "'}) RETURN a;"
                doel = self.tx_context.run(query).data()
                if len(doel) == 0:
                    ex.message = f'Doel agent is missing: {doel_uuid}'
                    ex.agent_uuids.append(doel_uuid)

            if json_dict['RelatieObject.bron']['@type'] == 'http://purl.org/dc/terms/Agent':
                query = "MATCH (a:Agent {uuid: '" + bron_uuid + "'}) RETURN a;"
                bron = self.tx_context.run(query).data()
                if len(bron) == 0:
                    ex.message = f'Bron agent is missing: {bron_uuid}'
                    ex.agent_uuids.append(bron_uuid)
            else:
                query = "MATCH (a:Asset {uuid: '" + bron_uuid + "'}) RETURN a;"
                bron = self.tx_context.run(query).data()
                if len(bron) == 0:
                    ex.message = f'Bron asset is missing: {bron_uuid}'
                    ex.asset_uuids.append(bron_uuid)
            raise ex
