import logging
from collections import namedtuple
from unittest import TestCase, mock

from neo4j.graph import Node

from AgentSyncer import AgentSyncer
from EventProcessors.ActiefGewijzigdProcessor import ActiefGewijzigdProcessor
from EventProcessors.AssetRelatiesGewijzigdProcessor import AssetRelatiesGewijzigdProcessor
from EventProcessors.BetrokkeneRelatiesGewijzigdProcessor import BetrokkeneRelatiesGewijzigdProcessor
from EventProcessors.CommentaarGewijzigdProcessor import CommentaarGewijzigdProcessor
from EventProcessors.EigenschappenGewijzigdProcessor import EigenschappenGewijzigdProcessor
from EventProcessors.GeometrieOrLocatieGewijzigdProcessor import GeometrieOrLocatieGewijzigdProcessor
from EventProcessors.NaamGewijzigdProcessor import NaamGewijzigdProcessor
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor
from EventProcessors.NieuweInstallatieProcessor import NieuweInstallatieProcessor
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.SchadebeheerderGewijzigdProcessor import SchadebeheerderGewijzigdProcessor
from EventProcessors.ToestandGewijzigdProcessor import ToestandGewijzigdProcessor
from EventProcessors.ToezichtGewijzigdProcessor import ToezichtGewijzigdProcessor
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from UnitTests.ResponseDouble import ResponseDouble


class EventProcessorsTests(TestCase):
    """These tests require a running instance of neo4J, defined in the setUp method"""

    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
        self.feedEventsProcessor = FeedEventsProcessor(neo4J_connector=self.connector, em_infra_importer=mock.Mock())
        self.tx_context = self.connector.start_transaction()

    def tearDown(self) -> None:
        self.tx_context.rollback()
        self.setUp()

    def test_nieuw_onderdeel(self):
        self.setUp()

        uuid = '00000000-0000-0000-0000-000000000001'

        processor = NieuwOnderdeelProcessor(self.tx_context, mock.Mock())
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        result = self.tx_context.run("MATCH (n{uuid:'" + uuid + "'}) return n").single()[0]

        self.assertTrue(isinstance(result, Node))
        self.assertIn('onderdeel', result.labels)
        self.assertIn('Asset', result.labels)
        self.assertIn('Netwerkpoort', result.labels)
        self.assertEqual(uuid, result._properties['assetId.identificator'][0:36])
        self.assertEqual('https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort', result._properties['typeURI'])

        self.tearDown()

    def test_nieuwe_installatie(self):
        self.setUp()

        uuid = '00000000-0000-0000-0000-000000000002'

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
        uuid = '00000000-0000-0000-0000-000000000001'
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
        uuid = '00000000-0000-0000-0000-000000000002'
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
        uuid = '00000000-0000-0000-0000-000000000001'
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
        uuid = '00000000-0000-0000-0000-000000000001'
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
        uuid = '00000000-0000-0000-0000-000000000001'
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

    def test_assetrelaties_gewijzigd(self):
        self.setUp()

        # create test assets
        uuids = ['00000000-0000-0000-0000-000000000001', 'bbac4a9a-905a-4991-bafa-43126fb5db10',
                 'c531aad8-e7c3-49f6-8c0d-c228a0c17c02']
        asset_processor = NieuwAssetProcessor()
        asset_processor.tx_context = self.tx_context
        for uuid in uuids:
            asset_processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # create test relation
        relatie_processor = RelatieProcessor()
        relatie_processor.tx_context = self.tx_context
        relatie_processor.create_assetrelatie_from_jsonLd_dict(
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + uuids[0]][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuids[0] + "'})-[r]-() return r"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HoortBij',
                         result_before_event._properties['typeURI'])

        # make the change
        relatie_processor = AssetRelatiesGewijzigdProcessor(tx_context=self.tx_context, emInfraImporter=mock.Mock())
        relatie_processor.process_dicts(
            assetrelatie_dicts=ResponseDouble.endpoint_changed['otl/assetrelaties/search/' + uuids[0]], uuids=uuids)

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging',
                         result_after_event._properties['typeURI'])

        self.tearDown()

    def test_betrokkenerelaties_gewijzigd(self):
        self.setUp()

        # create test assets
        uuids = ['00000000-0000-0000-0000-000000000001']
        asset_processor = NieuwAssetProcessor()
        asset_processor.tx_context = self.tx_context
        for uuid in uuids:
            asset_processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # create test agents
        agent_syncer = AgentSyncer(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        agent_syncer.tx_context = self.tx_context
        agent_uuids = ['a9d7c44c-0daf-4d3a-bffc-074afb5f54c0', '35de1da1-8ef3-45bf-bf91-cdb23e0889cc']
        for agent_uuid in agent_uuids:
            agent_syncer.update_agents(ResponseDouble.endpoint_orig['otl/agents/search/' + agent_uuid])

        # create test relation
        relatie_processor = RelatieProcessor()
        relatie_processor.tx_context = self.tx_context
        relatie_processor.remove_all_betrokkene_relaties(uuids)
        relatie_processor.create_betrokkenerelatie_from_jsonLd_dict(
            ResponseDouble.endpoint_orig['otl/betrokkenerelaties/search/' + uuids[0]][0])

        # test before change
        query = "MATCH (a:Agent) WHERE a.uuid in $agent_uuids return a"
        aantal_agents = self.tx_context.run(query, agent_uuids=agent_uuids).data()
        self.assertEqual(2, len(aantal_agents))
        query = "MATCH (a)-[r:HeeftBetrokkene]->() WHERE a.uuid in $uuids return r"
        result_before_event = self.tx_context.run(query, uuids=uuids).single()[0]
        self.assertEqual(agent_uuids[0], result_before_event._properties['doel.@id'].split('/')[-1][0:36])

        # make the change
        relatie_processor = BetrokkeneRelatiesGewijzigdProcessor(tx_context=self.tx_context, emInfraImporter=mock.Mock())
        relatie_processor.process_dicts(
            betrokkenerelatie_dicts=ResponseDouble.endpoint_changed['otl/betrokkenerelaties/search/' + uuids[0]], uuids=uuids)

        # test after change
        query = "MATCH (a)-[r:HeeftBetrokkene]->() WHERE a.uuid in $uuids return r"
        aantal_relaties = self.tx_context.run(query, uuids=uuids).data()
        self.assertEqual(1, len(aantal_relaties))
        query = "MATCH (a)-[r:HeeftBetrokkene]->() WHERE a.uuid in $uuids return r"
        result_after_event = self.tx_context.run(query, uuids=uuids).single()[0]
        self.assertEqual(agent_uuids[1], result_after_event._properties['doel.@id'].split('/')[-1][0:36])

        self.tearDown()

    def test_toezicht_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '00000000-0000-0000-0000-000000000002'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('vanascni', result_before_event._properties['tz:toezichter.tz:gebruikersnaam'])
        self.assertEqual('AWV_EW_AN', result_before_event._properties['tz:toezichtgroep.tz:referentie'])

        # make the change
        processor = ToezichtGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('bosmanja', result_after_event._properties['tz:toezichter.tz:gebruikersnaam'])
        self.assertEqual('EMT_TELE', result_after_event._properties['tz:toezichtgroep.tz:referentie'])

        self.tearDown()

    def test_schadebeheerder_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '00000000-0000-0000-0000-000000000002'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('District Geel', result_before_event._properties['tz:schadebeheerder.tz:naam'])
        self.assertEqual('114', result_before_event._properties['tz:schadebeheerder.tz:referentie'])

        # make the change
        processor = SchadebeheerderGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('District Brecht', result_after_event._properties['tz:schadebeheerder.tz:naam'])
        self.assertEqual('123', result_after_event._properties['tz:schadebeheerder.tz:referentie'])

        self.tearDown()

    def test_locatie_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '00000000-0000-0000-0000-000000000002'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('POINT Z (192721.4 201119.2 0)', result_before_event._properties['geometry'])
        self.assertEqual('Geel', result_before_event._properties['loc:puntlocatie.loc:weglocatie.loc:gemeente'])

        # make the change
        processor = GeometrieOrLocatieGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('POINT Z (150000 250000 0)', result_after_event._properties['geometry'])
        self.assertEqual('Antwerpen', result_after_event._properties['loc:puntlocatie.loc:weglocatie.loc:gemeente'])
        self.assertEqual('Antwerpen', result_after_event._properties['loc:puntlocatie.loc:adres.loc:provincie'])
        self.assertTrue('loc:puntlocatie.loc:adres.loc:nummer' not in result_after_event._properties)

        self.tearDown()

    def test_eigenschappen_gewijzigd(self):
        self.setUp()

        # create a test asset
        uuid = '00000000-0000-0000-0000-000000000001'
        processor = NieuwAssetProcessor()
        processor.tx_context = self.tx_context
        processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # test before change
        query = "MATCH (n{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('E', result_before_event._properties['config'])
        self.assertEqual(120, result_before_event._properties['nNILANCapaciteit'])
        self.assertEqual('BELFLANTLa_LS2.1', result_before_event._properties['naam'])
        self.assertEqual('https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort', result_before_event._properties['typeURI'])

        # make the change
        processor = EigenschappenGewijzigdProcessor(self.tx_context, mock.Mock())
        processor.process_dicts(ResponseDouble.endpoint_changed['otl/assets/search/' + uuid])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertTrue('config' not in result_after_event._properties)
        self.assertEqual(200, result_after_event._properties['nNILANCapaciteit'])
        self.assertEqual('BELFLANTLa_LS2.1', result_after_event._properties['naam'])
        self.assertEqual('in-gebruik', result_after_event._properties['toestand'])
        self.assertEqual('https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort', result_after_event._properties['typeURI'])
        self.assertEqual(len(result_before_event._properties), len(result_after_event._properties))

        self.tearDown()
