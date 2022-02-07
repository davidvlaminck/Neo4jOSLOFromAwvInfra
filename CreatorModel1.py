import json

from AbstractCreator import AbstractCreator


class CreatorModel1(AbstractCreator):
    def create_relatie_from_jsonLd_dict(self, json_dict):
        relatie_dict = {'assetIdUri': json_dict['@id'], 'typeURI': json_dict['@type'], 'isActief': json_dict["AIMDBStatus.isActief"],
                        'uuid' : json_dict['RelatieObject.assetId']['DtcIdentificator.identificator'][0:36]}

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
        asset_dict = {}
        for k, v in json_dict.items():
            if k == '@type':
                asset_dict['typeURI'] = v
            elif k == '@id':
                asset_dict['assetIdUri'] = v
            elif k.startswith('loc') or k == 'AIMObject.typeURI':
                continue
            elif k == 'AIMObject.assetId':
                asset_dict['assetId'] = json.dumps(v)
                asset_dict['uuid'] = v['DtcIdentificator.identificator'][0:36]
            elif k in ['AIMDBStatus.isActief', 'AIMNaamObject.naam', 'AIMObject.notitie', 'AIMToestand.toestand']:
                asset_dict[k.split('.')[1]] = v
            elif isinstance(v, dict):
                asset_dict[k] = json.dumps(v)
            else:
                asset_dict[k] = v
        asset_dict["geometry"] = self.get_wkt_from_puntlocatie(json_dict)
        if 'loc:Locatie.omschrijving' in json_dict.keys():
            asset_dict["loc:Locatie.omschrijving"] = json_dict['loc:Locatie.omschrijving']
        if 'loc:Locatie.geometrie' in json_dict.keys():
            geometrie = json_dict['loc:Locatie.geometrie']
            if geometrie != '':
                asset_dict["geometry"] = geometrie
        self.connector.perform_create_asset(asset_dict)

    @classmethod
    def get_wkt_from_puntlocatie(cls, json_dict):
        if 'loc:Locatie.puntlocatie' in json_dict.keys():
            puntlocatie = json_dict['loc:Locatie.puntlocatie']
            if "loc:3Dpunt.puntgeometrie" in puntlocatie:
                puntgeometrie = puntlocatie["loc:3Dpunt.puntgeometrie"]
                if "loc:DtcCoord.lambert72" in puntgeometrie:
                    coords = puntgeometrie["loc:DtcCoord.lambert72"]
                    return f'POINT Z ({coords["loc:DtcCoordLambert72.xcoordinaat"]} {coords["loc:DtcCoordLambert72.ycoordinaat"]} {coords["loc:DtcCoordLambert72.zcoordinaat"]})'
        return ''

