import logging

from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from Syncer import Syncer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    request_handler = RequestHandler(cert_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                                     key_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.key')
    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer)
    syncer.start_syncing()
