import json
import os
import sqlite3

import requests
from timeit import default_timer as timer

def make_rest_call():
    start = timer()
    cert_path = 'datamanager_eminfra_prd.awv.vlaanderen.be.crt'
    key_path = 'datamanager_eminfra_prd.awv.vlaanderen.be.key'
    url = "https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assets?pagingMode=CURSOR&size=500"
    response = requests.get(url, cert=(cert_path, key_path), headers={"accept": "application/vnd.awv.eminfra.v2+json"})
    decoded_string = response.content.decode("utf-8")
    end = timer()
    print(end - start)


    next_cursor = response.headers['em-paging-next-cursor']

    url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/assets?fromCursor={next_cursor}&pagingMode=CURSOR&size=10"
    response = requests.get(url, cert=(cert_path, key_path), headers={"accept": "application/vnd.awv.eminfra.v2+json"})
    decoded_string = response.content.decode("utf-8")
    #print(decoded_string)


class GraphSyncer:
    def __init__(self, path_db: str, cert_path: str, key_path: str):
        if not os.path.isfile(path_db):
            raise FileNotFoundError('database file not found')
        if not os.path.isfile(cert_path):
            raise FileNotFoundError('certificate file not found')
        if not os.path.isfile(key_path):
            raise FileNotFoundError('key file not found')
        self.path_db = path_db
        self.cert_path = cert_path
        self.key_path = key_path
        self.cursor = ''

    def start_sync(self):
        self.sync_agents()
        self.sync_assets()
        self.sync_relaties()

    def sync_relaties(self):
        self.perform_execute_query('DELETE FROM relaties')
        self.sync_assetrelaties()
        self.sync_betrokkenerelaties()

    def sync_betrokkenerelaties(self):
        start = timer()
        while True:
            betrokkenerelaties_data = self.get_betrokkenerelaties_from_olso_endpoints()
            if self.cursor == '':
                self.process_betrokkenerelaties_data(betrokkenerelaties_data)
                break
            self.process_betrokkenerelaties_data(betrokkenerelaties_data)
        end = timer()
        print("sync_betrokkenerelaties: " + str(end - start))

    def sync_assetrelaties(self):
        start = timer()
        while True:
            assetrelaties_data = self.get_assetrelaties_from_olso_endpoints()
            if self.cursor == '':
                self.process_assetrelaties_data(assetrelaties_data)
                break
            self.process_assetrelaties_data(assetrelaties_data)
        end = timer()
        print("sync_assetrelaties: " + str(end - start))

    def sync_assets(self):
        start = timer()
        self.perform_execute_query('DELETE FROM assets')
        while True:
            assets_data = self.get_assets_from_olso_endpoints()
            if self.cursor == '':
                self.process_assets_data(assets_data)
                break
            self.process_assets_data(assets_data)
        end = timer()
        print("sync_assets: " + str(end - start))

    def sync_agents(self):
        start = timer()
        self.perform_execute_query('DELETE FROM agents')
        while True:
            agents_data = self.get_agents_from_olso_endpoints()
            if self.cursor == '':
                self.process_agents_data(agents_data)
                break
            self.process_agents_data(agents_data)
        end = timer()
        print("sync_agents: " + str(end - start))

    def perform_execute_query(self, query):
        conn = sqlite3.connect(self.path_db)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()

    def process_betrokkenerelaties_data(self, betrokkenerelaties_data: [str]):
        for betrokkenerelatie_data in betrokkenerelaties_data:
            betrokkenerelatie_uuid = betrokkenerelatie_data['@id'].split('/')[-1][0:36]
            betrokkenerelatie_id = betrokkenerelatie_data['@id']
            typeURI = betrokkenerelatie_data['@type']
            actief = betrokkenerelatie_data['AIMDBStatus.isActief']
            if actief:
                actief = 1
            else:
                actief = 0
            bronId = betrokkenerelatie_data['RelatieObject.bron']['@id'].split('/')[-1]
            bronUuid = bronId[0:36]

            doelId = betrokkenerelatie_data['RelatieObject.doel']['@id'].split('/')[-1]
            doelUuid = doelId[0:36]

            rol = ''
            if 'HeeftBetrokkene.rol' in betrokkenerelatie_data:
                rol = betrokkenerelatie_data['HeeftBetrokkene.rol'].split('/')[-1]

            jsonld = json.dumps(betrokkenerelatie_data, ensure_ascii=False).replace("'", "''")

            query = f"INSERT INTO relaties (uuid, id, bronUuid, bronId, doelUuid, doelId, typeURI, actief, rol, jsonld) VALUES ('" \
                    f"{betrokkenerelatie_uuid}','{betrokkenerelatie_id}','{bronUuid}','{bronId}','{doelUuid}','{doelId}','{typeURI}','{actief}', '{rol}', '{jsonld}')"
            self.perform_execute_query(query)


    def process_assetrelaties_data(self, assetrelaties_data: [str]):
        for assetrelatie_data in assetrelaties_data:
            assetrelatie_uuid = assetrelatie_data['@id'].split('/')[-1][0:36]
            assetrelatie_id = assetrelatie_data['@id']
            typeURI = assetrelatie_data['@type']
            actief = assetrelatie_data['AIMDBStatus.isActief']
            if actief:
                actief = 1
            else:
                actief = 0
            bronId = assetrelatie_data['RelatieObject.bronAssetId']['DtcIdentificator.identificator']
            bronUuid = bronId[0:36]

            doelId = assetrelatie_data['RelatieObject.doelAssetId']['DtcIdentificator.identificator']
            doelUuid = doelId[0:36]

            jsonld = json.dumps(assetrelatie_data, ensure_ascii=False).replace("'", "''")

            query = f"INSERT INTO relaties (uuid, id, bronUuid, bronId, doelUuid, doelId, typeURI, actief, rol, jsonld) VALUES ('" \
                    f"{assetrelatie_uuid}','{assetrelatie_id}','{bronUuid}','{bronId}','{doelUuid}','{doelId}','{typeURI}','{actief}', NULL, '{jsonld}')"
            self.perform_execute_query(query)

    def process_assets_data(self, assets_data: [str]):
        for asset_data in assets_data:
            asset_uuid = asset_data['@id'].split('/')[-1][0:36]
            asset_id = asset_data['@id']
            typeURI = asset_data['@type']
            naampad = ''
            if 'NaampadObject.naampad' in asset_data:
                naampad = asset_data['NaampadObject.naampad']
            actief = asset_data['AIMDBStatus.isActief']
            if actief:
                actief = 1
            else:
                actief = 0
            toestand = asset_data["AIMToestand.toestand"].replace('https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/','')
            naam = ''
            if 'AIMNaamObject.naam' in asset_data:
                naam = asset_data['AIMNaamObject.naam']
            jsonld = json.dumps(asset_data, ensure_ascii=False).replace("'","''")

            query = f"INSERT INTO assets(uuid, id, typeURI, toestand, actief, naam, naampad, parent, jsonld) VALUES ('" \
                    f"{asset_uuid}','{asset_id}','{typeURI}','{toestand}','{actief}','{naam}','{naampad}', NULL, '{jsonld}')"
            self.perform_execute_query(query)

    def process_agents_data(self, agents_data: [str]):
        for agent_data in agents_data:
            agent_uuid = agent_data['@id'].split('/')[-1][0:36]
            agent_id = agent_data['@id']
            naam = agent_data['purl:Agent.naam'].replace("'","''")
            jsonld = json.dumps(agent_data, ensure_ascii=False).replace("'","''")

            query = f"INSERT INTO agents(uuid, id, naam, jsonld) VALUES ('{agent_uuid}','{agent_id}','{naam}','{jsonld}')"
            self.perform_execute_query(query)

    def get_objects_from_oslo_endpoint(self, size:int, url_part:str):
        url = f"https://services.apps.mow.vlaanderen.be/eminfra/core/api/otl/{url_part}?pagingMode=CURSOR&size={size}"
        if self.cursor != '':
            url += f'&fromCursor={self.cursor}'
        response = requests.get(url, cert=(self.cert_path, self.key_path),
                                headers={"accept": "application/vnd.awv.eminfra.v2+json"})
        decoded_string = response.content.decode("utf-8")
        dict_obj = json.loads(decoded_string)
        keys = response.headers.keys()
        if 'em-paging-next-cursor' in keys:
            self.cursor = response.headers['em-paging-next-cursor']
        else:
            self.cursor = ''
        return dict_obj['@graph']

    def get_betrokkenerelaties_from_olso_endpoints(self):
        return self.get_objects_from_oslo_endpoint(size=50, url_part='betrokkenerelaties')

    def get_assetrelaties_from_olso_endpoints(self):
        return self.get_objects_from_oslo_endpoint(size=500, url_part='assetrelaties')

    def get_agents_from_olso_endpoints(self):
        return self.get_objects_from_oslo_endpoint(size=500, url_part='agents')

    def get_assets_from_olso_endpoints(self):
        return self.get_objects_from_oslo_endpoint(size=500, url_part='assets')

if __name__ == '__main__':
    syncer = GraphSyncer(path_db=r'C:\resources\syncedGraphsAWVInfra.db',
                         cert_path = 'datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                         key_path = 'datamanager_eminfra_prd.awv.vlaanderen.be.key')
    syncer.start_sync()
