import json
import unittest

from EMInfraImporter import EMInfraImporter
from EventProcessors.AssetRelatiesGewijzigdProcessor import AssetRelatiesGewijzigdProcessor
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager


class AssetRelatiesGewijzigdProcessorTests(unittest.TestCase):
    def test_find_assets_to_resync_after_error(self):
        connector = Neo4JConnector(uri="bolt://localhost:7687", user="neo4jPython", password="python")
        settings_manager = SettingsManager(settings_path="C:\\resources\\settings_neo4jmodelcreator.json")

        requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type="JWT", env="prd")
        request_handler = RequestHandler(requester)

        eminfra_importer = EMInfraImporter(request_handler)

        dict_obj = json.loads('[{"@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Voedt", "@id": "https://data.awvvlaanderen.be/id/assetrelatie/5b35d003-1b9e-42d9-aaf7-bd32d1a7e603-b25kZXJkZWVsI1ZvZWR0", "RelatieObject.bron": {"@type": "https://lgc.data.wegenenverkeer.be/ns/installatie#Kast", "@id": "https://data.awvvlaanderen.be/id/asset/01c3942f-30df-4a02-a931-75e0f46937b6-bGdjOmluc3RhbGxhdGllI0thc3Q"}, "RelatieObject.doel": {"@type": "https://lgc.data.wegenenverkeer.be/ns/installatie#PLCLegacy", "@id": "https://data.awvvlaanderen.be/id/asset/33b43528-a932-4724-a50a-69af525f63fb-bGdjOmluc3RhbGxhdGllI1BMQ0xlZ2FjeQ"}, "RelatieObject.doelAssetId": {"DtcIdentificator.identificator": "33b43528-a932-4724-a50a-69af525f63fb-bGdjOmluc3RhbGxhdGllI1BMQ0xlZ2FjeQ", "DtcIdentificator.toegekendDoor": "AWV"}, "RelatieObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Voedt", "AIMDBStatus.isActief": true, "RelatieObject.bronAssetId": {"DtcIdentificator.toegekendDoor": "AWV", "DtcIdentificator.identificator": "01c3942f-30df-4a02-a931-75e0f46937b6-bGdjOmluc3RhbGxhdGllI0thc3Q"}, "RelatieObject.assetId": {"DtcIdentificator.toegekendDoor": "AWV", "DtcIdentificator.identificator": "5b35d003-1b9e-42d9-aaf7-bd32d1a7e603-b25kZXJkZWVsI1ZvZWR0"}}]')
        argp = AssetRelatiesGewijzigdProcessor(emInfraImporter=eminfra_importer, tx_context=connector.start_transaction())
        argp.find_assets_to_resync_after_error(dict_obj)