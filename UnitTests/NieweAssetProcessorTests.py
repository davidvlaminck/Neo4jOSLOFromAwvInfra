import unittest

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager


class NieweAssetProcessorTests(unittest.TestCase):
    def test_filter_out_existing_assets(self):
        connector = Neo4JConnector(uri="bolt://localhost:7687", user="neo4jPython", password="python")
        settings_manager = SettingsManager(settings_path="C:\\resources\\settings_neo4jmodelcreator.json")

        requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type="JWT", env="prd")
        request_handler = RequestHandler(requester)

        eminfra_importer = EMInfraImporter(request_handler)

        uuids = ["0008ab72-8f64-4f0c-84e8-98ff3b0609f2", "non-existing-uuid", "012aec29-d1c5-477b-8628-06072747240e"]
        nap = NieuwOnderdeelProcessor(emInfraImporter=eminfra_importer, tx_context=connector.start_transaction())
        filtered_uuids = nap.filter_out_existing_assets(uuids)
        self.assertListEqual(['non-existing-uuid'], filtered_uuids)