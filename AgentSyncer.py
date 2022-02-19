from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from Neo4JConnector import Neo4JConnector


class AgentSyncer:
    def __init__(self, neo4J_connector: Neo4JConnector, emInfraImporter: EMInfraImporter):
        self.neo4J_connector = neo4J_connector
        self.emInfraImporter = emInfraImporter
        self.tx_context = None

    def sync_agents(self):
        self.tx_context = self.neo4J_connector.start_transaction()
        self.update_all_agents()
        self.neo4J_connector.commit_transaction(self.tx_context)

    def update_all_agents(self):
        agents = self.get_all_agents()
        self.update_agents(agent_dicts=agents)

    def get_all_agents(self) -> []:
        return self.emInfraImporter.import_all_agents_from_webservice()

    def update_agents(self, agent_dicts: [dict], chunk_size: int = 20):
        if len(agent_dicts) == 0:
            return
        flattened_dicts = self.clean_agent_dicts(agent_dicts)

        list_id_uris = list(map(lambda x: x['assetIdUri'], flattened_dicts))
        existing_nodes = self.tx_context.run("MATCH (a:Agent) WHERE a.assetIdUri IN $params RETURN a", params=list_id_uris).data()
        existing_id_uris = []
        if len(existing_nodes) > 0:
            l = list(map(lambda x: x['a'], existing_nodes))
            existing_id_uris = list(map(lambda x: x['assetIdUri'], l))

        # filter which must be created and what must be updated
        dicts_to_create = []
        dicts_to_update = []
        for agent in flattened_dicts:
            if agent['assetIdUri'] in existing_id_uris:
                dicts_to_update.append(agent)
            else:
                dicts_to_create.append(agent)

        # create agents
        for i in range(0, len(dicts_to_create), chunk_size):
            chunk = dicts_to_create[i:i + chunk_size]
            self.tx_context.run("UNWIND $params AS map CREATE (a:Agent) SET a = map", params=chunk)

        # update agents
        for i in range(0, len(dicts_to_update), chunk_size):
            chunk = dicts_to_update[i:i + chunk_size]
            self.tx_context.run("UNWIND $params AS map MATCH (a:Agent) WHERE a.assetIdUri = map.assetIdUri SET a = map", params=chunk)

    def clean_agent_dicts(self, agent_dicts):
        flattened_dicts = []
        for agent_dict in agent_dicts:
            old_dict = NieuwAssetProcessor().flatten_dict(input_dict=agent_dict)
            new_dict = {}
            for k, v in old_dict.items():
                if k == '@type':
                    new_dict[k] = v
                    continue

                if k == '@id':
                    new_dict['assetIdUri'] = v
                    new_dict['uuid'] = v.split('/')[-1][0:36]
                    continue

                if ':' in k:
                    new_dict[k.split(':')[-1]] = v
                else:
                    new_dict[k] = v

            flattened_dicts.append(new_dict)

        return flattened_dicts

