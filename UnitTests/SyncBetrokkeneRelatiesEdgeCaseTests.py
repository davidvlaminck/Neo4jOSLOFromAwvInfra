import logging
from unittest import TestCase, mock

from AgentSyncer import AgentSyncer
from EventProcessors.BetrokkeneRelatiesGewijzigdProcessor import BetrokkeneRelatiesGewijzigdProcessor
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from UnitTests.ResponseDouble import ResponseDouble


class SyncBetrokkeneRelatiesEdgeCaseTests(TestCase):
    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
        self.feedEventsProcessor = FeedEventsProcessor(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        self.tx_context = self.connector.start_transaction()

    def tearDown(self) -> None:
        self.tx_context.rollback()
        self.setUp()

    def test_betrokkenerelaties_gewijzigd(self):
        self.setUp()

        # create test assets
        uuids = ['000a35d5-c4a5-4a36-8620-62c99e053ba0']
        asset_processor = NieuwAssetProcessor()
        asset_processor.tx_context = self.tx_context
        for uuid in uuids:
            asset_processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        # create test agents
        agent_syncer = AgentSyncer(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        agent_syncer.tx_context = self.tx_context
        agent_uuids = ['a9d7c44c-0daf-4d3a-bffc-074afb5f54c0']
        for agent_uuid in agent_uuids:
            agent_syncer.update_agents(ResponseDouble.endpoint_orig['otl/agents/search/' + agent_uuid])

        # create test relation
        relatie_processor = RelatieProcessor()
        relatie_processor.tx_context = self.tx_context
        relatie_processor.create_betrokkenerelatie_from_jsonLd_dict(
            ResponseDouble.endpoint_orig['otl/betrokkenerelaties/search/' + uuids[0]][0])

        # test before change
        query = "MATCH (a:Agent) WHERE a.uuid in $agent_uuids return a"
        aantal_agents = self.tx_context.run(query, agent_uuids=agent_uuids).data()
        self.assertEqual(1, len(aantal_agents))
        query = "MATCH (a)-[r:HeeftBetrokkene]->() WHERE a.uuid in $uuids return r"
        result_before_event = self.tx_context.run(query, uuids=uuids).single()[0]
        self.assertEqual(agent_uuids[0], result_before_event._properties['doel.@id'].split('/')[-1][0:36])

        # make the change
        relatie_processor = BetrokkeneRelatiesGewijzigdProcessor(tx_context=self.tx_context, emInfraImporter=mock.Mock())
        with self.assertRaises(RelationNotCreatedError):
            relatie_processor.process_dicts(
                betrokkenerelatie_dicts=ResponseDouble.endpoint_changed['otl/betrokkenerelaties/search/' + uuids[0]], uuids=uuids)

        self.tearDown()