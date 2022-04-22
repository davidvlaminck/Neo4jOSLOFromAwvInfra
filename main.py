import logging

from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from Syncer import Syncer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    settings_manager = SettingsManager(settings_path='C:\\resources\\settings_neo4jmodelcreator.json')

    requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type='JWT', env='prd')
    request_handler = RequestHandler(requester)

    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer)
    syncer.start_syncing()
