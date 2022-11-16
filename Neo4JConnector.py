import logging
import time

from neo4j import GraphDatabase, Transaction


class Neo4JConnector:
    def __init__(self, uri, user, password, database: str = 'neo4j'):
        self.driver = GraphDatabase.driver(uri=uri, auth=(user, password))
        self.db = database

    def get_page_by_get_or_create_params(self):
        with self.driver.session(database=self.db) as session:
            params = session.run("MATCH (p:Params) RETURN p").single()
            if params is None:
                self.set_default_constraints_and_indices(session)
                params = session.run("CREATE (p:Params {page:-1, event_id:'', pagesize:100, "
                                     "freshstart:True, otltype:-1, cursor:''}) RETURN p").single()
            return params[0]

    @staticmethod
    def save_props_to_params(tx: Transaction, params: dict):
        tx.run(f"MATCH (p:Params) SET p += $params", params=params)

    @staticmethod
    def update_params(tx: Transaction, page_num: int, event_id: int):
        tx.run(f"MATCH (p:Params) SET p.page = {page_num}, p.event_id = '{event_id}'")

    def close(self):
        self.driver.close()

    def perform_create_asset(self, params: dict, ns: str, assettype: str):
        with self.driver.session(database=self.db) as session:
            tx = session.begin_transaction()
            self._create_asset_by_dict(tx, params, ns, assettype)
            tx.commit()
            tx.close()

    def perform_create_relatie(self, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        with self.driver.session(database=self.db) as session:
            session.write_transaction(self._create_relatie_by_dict, bron_uuid=bron_uuid, doel_uuid=doel_uuid,
                                      relatie_type=relatie_type, params=params)

    @staticmethod
    def _create_asset_by_dict(tx, params: dict, ns: str, assettype: str):
        result = tx.run(f"CREATE (a:Asset:{ns}:{assettype} $params) ", params=params)
        return result

    @staticmethod
    def _create_relatie_by_dict(tx, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        query = f'''\
                MATCH (a:Asset), (b:Asset) 
                WHERE a.uuid = "{bron_uuid}" 
                AND b.uuid = "{doel_uuid}" 
                CREATE (a)-[r:{relatie_type} $params]->(b) 
                RETURN type(r), r.name
                '''
        result = tx.run(query, params=params)
        return result

    def start_transaction(self) -> Transaction:
        return self.driver.session(database=self.db).begin_transaction()

    @staticmethod
    def commit_transaction(tx_context: Transaction):
        tx_context.commit()
        tx_context.close()

    @staticmethod
    def set_default_constraints_and_indices(session: Transaction):
        session.run("CREATE CONSTRAINT Asset_uuid IF NOT EXISTS FOR (n:Asset) REQUIRE n.uuid IS UNIQUE")
        session.run("CREATE CONSTRAINT Agent_uuid IF NOT EXISTS FOR (n:Agent) REQUIRE n.uuid IS UNIQUE")

    def query(self, query):
        assert self.driver is not None, "Driver not initialized!"
        session = None

        while True:
            try:
                session = self.driver.session(database=self.db)
                response = list(session.run(query))
                return response
            except Exception as e:
                logging.error("Query failed:", e)
                logging.error('Are settings and/or connection to the Neo4J database okay?')
                logging.info('Retrying in 30 seconds.')
                time.sleep(30)
            finally:
                if session is not None:
                    session.close()
