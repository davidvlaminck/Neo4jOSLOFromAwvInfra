import json

from AbstractCreator import AbstractCreator


class CreatorModel1(AbstractCreator):
    def create_relatie_from_jsonLd_dict(self, json_dict):
        relatie_dict = {'assetIdUri': json_dict['@id'], 'typeURI': json_dict['@type'], 'isActief': json_dict["AIMDBStatus.isActief"],
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

        self.connector.perform_create_relatie(bron_uuid=bron_uuid, doel_uuid=doel_uuid, relatie_type=relatie_type,
                                              params=relatie_dict)

    def create_asset_from_jsonLd_dict(self, json_dict):
        new_dict = {}
        for k, v in json_dict.items():
            if not k.startswith('ins') and not k.startswith('ond'):
                new_dict[k] = v

        json_dict = self.flatten_dict(new_dict)

        asset_dict = {}
        for k, v in json_dict.items():
            if k == '@type':
                continue
            elif k == '@id':
                asset_dict['assetIdUri'] = v
            else:
                asset_dict[k] = v

        asset_dict["uuid"] = asset_dict['assetId.identificator'][0:36]
        asset_dict["geometry"] = self.get_wkt_from_puntlocatie(json_dict)
        if 'geometrie' in json_dict.keys():
            geometrie = json_dict['geometrie']
            if geometrie != '' and asset_dict["geometry"] == '':
                asset_dict["geometry"] = geometrie
        korte_uri = asset_dict['typeURI'].split('/ns/')[1]
        ns = korte_uri.split('#')[0]
        assettype = korte_uri.split('#')[1]

        self.connector.perform_create_asset(params=asset_dict, ns=ns, assettype=assettype)

    @classmethod
    def get_wkt_from_puntlocatie(cls, json_dict):
        if 'puntlocatie.puntgeometrie.lambert72.xcoordinaat' in json_dict.keys():
            return f'POINT Z ({json_dict["puntlocatie.puntgeometrie.lambert72.xcoordinaat"]} ' \
                   f'{json_dict["puntlocatie.puntgeometrie.lambert72.ycoordinaat"]} ' \
                   f'{json_dict["puntlocatie.puntgeometrie.lambert72.zcoordinaat"]})'
        return ''

