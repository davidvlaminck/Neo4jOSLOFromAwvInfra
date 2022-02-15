import logging
from collections import namedtuple
from unittest import TestCase

from neo4j.graph import Node

from EMInfraImporter import EMInfraImporter
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler


class EventProcessorsTests(TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
        self.request_handler = RequestHandler(cert_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                                         key_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.key')
        self.eminfra_importer = EMInfraImporter(self.request_handler)
        self.processor = FeedEventsProcessor(neo4J_connector=self.connector, emInfraImporter=self.eminfra_importer)
        self.tx_context = self.connector.start_transaction()

    def tearDown(self) -> None:
        self.tx_context.rollback()

    def test_NieuweInstallatie(self):
        self.setUp()

        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'

        EventParams = namedtuple('EventParams', 'event_dict page_num full_sync')
        event_params = EventParams(event_dict={"NIEUWE_INSTALLATIE": [uuid]}, page_num=0, full_sync=True)

        self.processor.process_events_by_event_params(event_params, self.tx_context)

        result = self.tx_context.run("MATCH (n{uuid:'" + uuid + "'}) return n").single()[0]

        self.assertTrue(isinstance(result, Node))
        self.assertIn('onderdeel', result.labels)
        self.assertIn('Asset', result.labels)
        self.assertIn('Netwerkpoort', result.labels)
        self.assertEqual(uuid, result._properties['assetId.identificator'][0:36])

        self.tearDown()


