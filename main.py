import logging

from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from Syncer import Syncer

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    connector = Neo4JConnector(uri="bolt://localhost:7687", user="neo4jPython", password="python")
    settings_manager = SettingsManager(settings_path='.\\settings_neo4jmodelcreator.json')

    requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type='JWT', env='prd')
    request_handler = RequestHandler(requester)

    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer, settings=settings_manager.settings)
    syncer.start_syncing(stop_when_fully_synced=False)
