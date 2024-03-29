import logging
from unittest import TestCase, mock

from AgentSyncer import AgentSyncer
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from UnitTests.ResponseDouble import ResponseDouble


class AgentSyncerTests(TestCase):
    """These tests require a running instance of neo4J, defined in the setUp method"""
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
        self.feedEventsProcessor = FeedEventsProcessor(neo4J_connector=self.connector, em_infra_importer=mock.Mock())
        self.tx_context = self.connector.start_transaction()

    def tearDown(self) -> None:
        self.tx_context.rollback()
        self.setUp()

    def test_nieuwe_agent(self):
        self.setUp()

        syncer = AgentSyncer(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        syncer.tx_context = self.tx_context

        # test before change
        query = "MATCH (n:Agent{uuid:'a9d7c44c-0daf-4d3a-bffc-074afb5f54c0'}) return n"
        result_before_event = self.tx_context.run(query).single()
        self.assertIsNone(result_before_event)

        # make the change
        syncer.update_agents(ResponseDouble.endpoint_orig['otl/agents/search/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0'])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('Steve Desmadryl', result_after_event._properties['naam'])

        self.tearDown()

    def test_update_agent(self):
        self.setUp()

        syncer = AgentSyncer(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        syncer.tx_context = self.tx_context

        # create a test agent
        uuid = 'a9d7c44c-0daf-4d3a-bffc-074afb5f54c0'
        syncer.update_agents(ResponseDouble.endpoint_orig['otl/agents/search/' + uuid])

        # test before change
        query = "MATCH (n:Agent{uuid:'" + uuid + "'}) return n"
        result_before_event = self.tx_context.run(query).single()[0]
        self.assertEqual('Steve Desmadryl', result_before_event._properties['naam'])

        # make the change
        syncer.update_agents(ResponseDouble.endpoint_changed['otl/agents/search/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0'])

        # test after change
        result_after_event = self.tx_context.run(query).single()[0]
        self.assertEqual('nieuwe_naam', result_after_event._properties['naam'])

        self.tearDown()

    def test_create_and_update_agent(self):
        self.setUp()

        syncer = AgentSyncer(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        syncer.tx_context = self.tx_context

        # create a test agent
        uuid = 'a9d7c44c-0daf-4d3a-bffc-074afb5f54c0'
        syncer.update_agents(ResponseDouble.endpoint_orig['otl/agents/search/' + uuid])

        # test before change
        query = "MATCH (n:Agent) where n.uuid IN ['" + uuid + "','35de1da1-8ef3-45bf-bf91-cdb23e0889cc'] return n"
        query_result_data = self.tx_context.run(query).data()
        result_before_event = query_result_data[0]['n']
        self.assertEqual('Steve Desmadryl', result_before_event['naam'])
        self.assertEqual(1, len(query_result_data))

        # make the change
        agents_from_db_double = [ResponseDouble.endpoint_changed['otl/agents/search/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0'][0],
                                 ResponseDouble.endpoint_orig['otl/agents/search/35de1da1-8ef3-45bf-bf91-cdb23e0889cc'][0]]
        syncer.update_agents(agents_from_db_double)

        # test after change
        results_after_event = self.tx_context.run(query).data()
        results_after_event = list(map(lambda x: x['n'], results_after_event))
        uuids = list(map(lambda x: x['uuid'], results_after_event))
        results_dict = dict(zip(uuids, results_after_event))

        self.assertEqual('nieuwe_naam', results_dict['a9d7c44c-0daf-4d3a-bffc-074afb5f54c0']['naam'])
        self.assertEqual('EMT_TELE', results_dict['35de1da1-8ef3-45bf-bf91-cdb23e0889cc']['naam'])

        self.tearDown()
