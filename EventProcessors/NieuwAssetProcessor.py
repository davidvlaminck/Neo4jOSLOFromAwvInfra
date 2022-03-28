class NieuwAssetProcessor:
    def __init__(self):
        self.tx_context = None

    @staticmethod
    def create_asset_by_dict(tx, params: dict, ns: str, assettype: str):
        if '-' in assettype:
            assettype = '`' + assettype + '`'
        tx.run(f"CREATE (a:Asset:{ns}:{assettype} $params) ", params=params)

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

        if 'assetId.identificator' not in asset_dict:
            asset_dict["uuid"] = asset_dict['assetIdUri'].split('/asset/')[1][0:36]
        else:
            asset_dict["uuid"] = asset_dict['assetId.identificator'][0:36]

        if 'typeURI' not in asset_dict:
            asset_dict['typeURI'] = json_dict['@type']

        asset_dict["geometry"] = self.get_wkt_from_puntlocatie(json_dict)
        if 'loc:geometrie' in json_dict.keys():
            geometrie = json_dict['loc:geometrie']
            if geometrie != '' and asset_dict["geometry"] == '':
                asset_dict["geometry"] = geometrie
        korte_uri = asset_dict['typeURI'].split('/ns/')[1]
        ns = korte_uri.split('#')[0]
        assettype = korte_uri.split('#')[1]

        self.create_asset_by_dict(self.tx_context, params=asset_dict, ns=ns, assettype=assettype)

    @staticmethod
    def get_wkt_from_puntlocatie(json_dict):
        if 'loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:xcoordinaat' in json_dict.keys():
            return f'POINT Z ({json_dict["loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:xcoordinaat"]} ' \
                   f'{json_dict["loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:ycoordinaat"]} ' \
                   f'{json_dict["loc:puntlocatie.loc:puntgeometrie.loc:lambert72.loc:zcoordinaat"]})'
        return ''

    def flatten_dict(self, input_dict: dict, separator: str = '.', prefix='', affix='', new_dict=None):
        """Takes a dictionary as input and recursively flattens dict and list values by using the dotnotation.
        This removes the prefix from the jsonLD: 'AIMDBStatus.isActief' -> 'isActief' but keeps the namespaces of OEF
        Also trims the uri values of choices"""
        if new_dict is None:
            new_dict = {}
        for k, v in input_dict.items():
            if '.' in k:
                ns = ''
                if ':' in k:
                    ns = k.split(':')[0] + ':'
                k = ns + k.split('.')[1]
            if isinstance(v, dict):
                if prefix != '':
                    self.flatten_dict(input_dict=v, prefix=(prefix + affix + '#sep#' + k), new_dict=new_dict)
                else:
                    self.flatten_dict(input_dict=v, prefix=k, new_dict=new_dict)
            elif isinstance(v, list):
                for i in range(0, len(v)):
                    if isinstance(v[i], dict):
                        if prefix != '':
                            self.flatten_dict(input_dict=v[i], prefix=(prefix + affix + '#sep#' + k), affix='[' + str(i) + ']',
                                              new_dict=new_dict)
                        else:
                            self.flatten_dict(input_dict=v[i], prefix=(k), affix='[' + str(i) + ']', new_dict=new_dict)
                    else:
                        if isinstance(v[i], str) and 'id/concept/' in v[i]:
                            v[i] = v[i].split('/')[-1]
                        if prefix != '':
                            new_dict[prefix + '#sep#' + k + '[' + str(i) + ']'] = v[i]
                        else:
                            new_dict[k + '[' + str(i) + ']'] = v[i]
            else:
                if isinstance(v, str) and 'id/concept/' in v:
                    v = v.split('/')[-1]
                if prefix != '':
                    new_dict[prefix + affix + '#sep#' + k] = v
                else:
                    new_dict[k] = v

        clean_dict = {}
        for k, v in new_dict.items():
            clean_dict[k.replace('#sep#', separator)] = v

        return clean_dict
