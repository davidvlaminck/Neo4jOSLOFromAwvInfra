import logging
from collections import namedtuple
from unittest import TestCase, mock

from neo4j.graph import Node

from EMInfraImporter import EMInfraImporter
from EventProcessors.ActiefGewijzigdProcessor import ActiefGewijzigdProcessor
from EventProcessors.CommentaarGewijzigdProcessor import CommentaarGewijzigdProcessor
from EventProcessors.NaamGewijzigdProcessor import NaamGewijzigdProcessor
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor
from EventProcessors.NieuweInstallatieProcessor import NieuweInstallatieProcessor
from EventProcessors.ToestandGewijzigdProcessor import ToestandGewijzigdProcessor
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from UnitTests.ResponseDouble import ResponseDouble


class EventProcessorsTests(TestCase):
    """These tests require a running instance of neo4J, defined in the setUp method"""
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
        self.feedEventsProcessor = FeedEventsProcessor(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        self.tx_context = self.connector.start_transaction()

    def tearDown(self) -> None:
        self.tx_context.rollback()
        self.setUp()

    def test_nieuw_onderdeel(self):
        self.setUp()

        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'

        processor = NieuwOnderdeelProcessor(self.tx_context, mock.Mock())
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        result = self.tx_context.run("MATCH (n{uuid:'" + uuid + "'}) return n").single()[0]

        self.assertTrue(isinstance(result, Node))
        self.assertIn('onderdeel', result.labels)
        self.assertIn('Asset', result.labels)
        self.assertIn('Netwerkpoort', result.labels)
        self.assertEqual(uuid, result._properties['assetId.identificator'][0:36])

        self.tearDown()

    def test_nieuwe_installatie(self):
        self.setUp()

        uuid = '00000453-56ce-4f8b-af44-960df526cb30'

        processor = NieuweInstallatieProcessor(self.tx_context, mock.Mock())
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        result = self.tx_context.run("MATCH (n{uuid:'" + uuid + "'}) return n").single()[0]

        self.assertTrue(isinstance(result, Node))
        self.assertIn('installatie', result.labels)
        self.assertIn('Asset', result.labels)
        self.assertIn('Kast', result.labels)
        self.assertEqual(uuid, result._properties['assetId.identificator'][0:36])

        self.tearDown()

    def test_naam_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('BELFLANTLa_LS2.1', result_before_event._properties['naam'])

        # make the change
        processor = NaamGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('nieuwe_naam', result_after_event._properties['naam'])
        self.assertFalse('naampad' in result_after_event._properties)

        self.tearDown()

    def test_naampad_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '00000453-56ce-4f8b-af44-960df526cb30'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('057A5/KAST', result_before_event._properties['naampad'])
        self.assertEqual('KAST', result_before_event._properties['naam'])

        # make the change
        processor = NaamGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('057A5/057A5.K', result_after_event._properties['naampad'])
        self.assertEqual('057A5.K', result_after_event._properties['naam'])

        self.tearDown()

    def test_actief_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual(True, result_before_event._properties['isActief'])

        # make the change
        processor = ActiefGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual(False, result_after_event._properties['isActief'])

        self.tearDown()

    def test_toestand_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('in-gebruik', result_before_event._properties['toestand'])

        # make the change
        processor = ToestandGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('verwijderd', result_after_event._properties['toestand'])

        self.tearDown()

    def test_commentaar_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '000a35d5-c4a5-4a36-8620-62c99e053ba0'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('', result_before_event._properties['notitie'])

        # make the change
        processor = CommentaarGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('aangepaste notitie', result_after_event._properties['notitie'])

        self.tearDown()
