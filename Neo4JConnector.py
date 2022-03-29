from neo4j import GraphDatabase, Transaction


class Neo4JConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_page_by_get_or_create_params(self):
        with self.driver.session() as session:
            params = session.run("MATCH (p:Params) RETURN p").single()
            if params is None:
                params = session.run("CREATE (p:Params {page:-1, event_id:-1, pagesize:100, freshstart:True, otltype:-1, cursor:''}) RETURN p").single()
            return params[0]

    def save_props_to_params(self, params: dict):
        with self.driver.session() as session:
            tx = session.begin_transaction()
            tx.run(f"MATCH (p:Params) SET p += $params", params=params)
            tx.commit()
            tx.close()

    def update_params(self, tx: Transaction, page_num: int, event_id: int):
        tx.run(f"MATCH (p:Params) SET p.page = {page_num}, event_id = {event_id}")

    def close(self):
        self.driver.close()

    def perform_create_asset(self, params: dict, ns: str, assettype: str):
        with self.driver.session() as session:
            tx = session.begin_transaction()
            self._create_asset_by_dict(tx, params, ns, assettype)
            tx.commit()
            tx.close()

    def perform_create_relatie(self, bron_uuid='', doel_uuid='', relatie_type='', params=None):
        with self.driver.session() as session:
            session.write_transaction(self._create_relatie_by_dict, bron_uuid=bron_uuid, doel_uuid=doel_uuid,
                                      relatie_type=relatie_type, params=params)

    @staticmethod
    def _create_asset_by_dict(tx, params: dict, ns: str, assettype: str):
        result = tx.run(f"CREATE (a:Asset:{ns}:{assettype} $params) ", params=params)
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

    def start_transaction(self) -> Transaction:
        return self.driver.session().begin_transaction()

    @staticmethod
    def commit_transaction(tx_context: Transaction):
        tx_context.commit()
        tx_context.close()

