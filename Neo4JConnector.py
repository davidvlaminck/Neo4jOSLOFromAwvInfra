from neo4j import GraphDatabase


class Neo4JConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def perform_create_asset(self, params: dict):
        with self.driver.session() as session:
            session.write_transaction(self._create_asset_by_dict, params)

    def perform_create_relatie(self, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        with self.driver.session() as session:
            session.write_transaction(self._create_relatie_by_dict, bron_uuid=bron_uuid, doel_uuid=doel_uuid,
                                      relatie_type=relatie_type, params=params)

    @staticmethod
    def _create_asset_by_dict(tx, params: dict):
        result = tx.run("CREATE (a:Asset $params) ", params=params)
        return result

    @staticmethod
    def _create_relatie_by_dict(tx, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        query = "MATCH (a:Asset), (b:Asset) " \
                f"WHERE a.uuid = '{bron_uuid}' " \
                f"AND b.uuid = '{doel_uuid}' " \
                f"CREATE (a)-[r:{relatie_type} " \
                "$params]->(b) " \
                f"RETURN type(r), r.name"
        result = tx.run(query, params=params)
        return result
