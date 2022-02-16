import json

from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor


class RelatieProcessor:
    def __init__(self):
        self.tx_context = None

    def remove_all_asset_relaties(self, asset_uuids: [str]):
        query = f"UNWIND $params as uuids " \
                "MATCH ({uuid: uuids})-[r]-() WHERE r <> 'HeeftBetrokkene' DELETE r"
        self.tx_context.run(query, params=asset_uuids)

    def remove_all_betrokkene_relaties(self, asset_uuids: [str]):
        query = f"UNWIND $params as uuids " \
                "MATCH ({uuid: uuids})-[r:HeeftBetrokkene]-() DELETE r"
        self.tx_context.run(query, params=asset_uuids)

    @staticmethod
    def _create_assetrelatie_by_dict(tx, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        query = "MATCH (a:Asset), (b:Asset) " \
                f"WHERE a.uuid = '{bron_uuid}' " \
                f"AND b.uuid = '{doel_uuid}' " \
                f"CREATE (a)-[r:{relatie_type} " \
                "$params]->(b) " \
                f"RETURN type(r), r.name"
        tx.run(query, params=params)

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

        self._create_assetrelatie_by_dict(tx=self.tx_context, bron_uuid=bron_uuid, doel_uuid=doel_uuid, relatie_type=relatie_type,
                                          params=relatie_dict)

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

        self._create_assetrelatie_by_dict(tx=self.tx_context, bron_uuid=bron_uuid, doel_uuid=doel_uuid, relatie_type=relatie_type,
                                          params=relatie_dict)

