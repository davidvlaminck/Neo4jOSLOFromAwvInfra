import logging
from collections import namedtuple
from unittest import TestCase

from neo4j.graph import Node

from EMInfraImporter import EMInfraImporter
from EventProcessors.ActiefGewijzigdProcessor import ActiefGewijzigdProcessor
from EventProcessors.CommentaarGewijzigdProcessor import CommentaarGewijzigdProcessor
from EventProcessors.NaamGewijzigdProcessor import NaamGewijzigdProcessor
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.ToestandGewijzigdProcessor import ToestandGewijzigdProcessor
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
        self.setUp()

    def test_NieuwOnderdeel(self):
        self.setUp()

        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'

        EventParams = namedtuple('EventParams', 'event_dict page_num full_sync')
        event_params = EventParams(event_dict={"NIEUW_ONDERDEEL": [uuid]}, page_num=0, full_sync=True)

        self.processor.process_events_by_event_params(event_params, self.tx_context)

        result = self.tx_context.run("MATCH (n{uuid:'" + uuid + "'}) return n").single()[0]

        self.assertTrue(isinstance(result, Node))
        self.assertIn('onderdeel', result.labels)
        self.assertIn('Asset', result.labels)
        self.assertIn('Netwerkpoort', result.labels)
        self.assertEqual(uuid, result._properties['assetId.identificator'][0:36])

        self.tearDown()

    def test_naam_gewijzigd(self):
        self.setUp()
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        paramsdict = {'uuid': uuid,
                      'naam': 'testnaam'}
        NieuwAssetProcessor.create_asset_by_dict(tx=self.tx_context, ns='onderdeel', assettype='Netwerkpoort', params=paramsdict)
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('testnaam', result_before_event._properties['naam'])

        processor = NaamGewijzigdProcessor(self.tx_context, self.eminfra_importer)
        processor.process_dicts([{'typeURI': 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort',
                                  'AIMNaamObject.naam': 'nieuwe_naam',
                                  'assetId.identificator': uuid}])

        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('nieuwe_naam', result_after_event._properties['naam'])
        self.assertFalse('naampad' in result_after_event._properties)

    def test_actief_gewijzigd(self):
        self.setUp()
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        paramsdict = {'uuid': uuid,
                      'isActief': True}
        NieuwAssetProcessor.create_asset_by_dict(tx=self.tx_context, ns='onderdeel', assettype='Netwerkpoort', params=paramsdict)
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual(True, result_before_event._properties['isActief'])

        processor = ActiefGewijzigdProcessor(self.tx_context, self.eminfra_importer)
        processor.process_dicts([{'typeURI': 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort',
                                  'AIMDBStatus.isActief': False,
                                  'assetId.identificator': uuid}])

        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual(False, result_after_event._properties['isActief'])

    def test_toestand_gewijzigd(self):
        self.setUp()
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        paramsdict = {'uuid': uuid,
                      'toestand': 'in-ontwerp'}
        NieuwAssetProcessor.create_asset_by_dict(tx=self.tx_context, ns='onderdeel', assettype='Netwerkpoort', params=paramsdict)
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('in-ontwerp', result_before_event._properties['toestand'])

        processor = ToestandGewijzigdProcessor(self.tx_context, self.eminfra_importer)
        processor.process_dicts([{'typeURI': 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort',
                                  'AIMToestand.toestand': 'https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/in-gebruik',
                                  'assetId.identificator': uuid}])

        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('in-gebruik', result_after_event._properties['toestand'])

    def test_commentaar_gewijzigd(self):
        self.setUp()
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        paramsdict = {'uuid': uuid,
                      'notitie': 'testnotitie'}
        NieuwAssetProcessor.create_asset_by_dict(tx=self.tx_context, ns='onderdeel', assettype='Netwerkpoort', params=paramsdict)
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('testnotitie', result_before_event._properties['notitie'])

        processor = CommentaarGewijzigdProcessor(self.tx_context, self.eminfra_importer)
        processor.process_dicts([{'typeURI': 'https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort',
                                  'AIMObject.notitie': 'nieuwe_notitie',
                                  'assetId.identificator': uuid}])

        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('nieuwe_notitie', result_after_event._properties['notitie'])
