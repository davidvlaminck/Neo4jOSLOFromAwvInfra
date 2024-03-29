import logging
from pathlib import Path

from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from Syncer import Syncer

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    connector = Neo4JConnector(uri="bolt://localhost:7687", user="neo4j", password="***", database='neo4j')
    settings_manager = SettingsManager(settings_path=Path('/home/david/Documents/AWV/resources/settings_neo4jmodelcreator.json'))
    # settings_manager = SettingsManager(settings_path='C:\\resources\\settings_neo4jmodelcreator.json')

    requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type='JWT', env='prd')
    request_handler = RequestHandler(requester)

    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer, settings=settings_manager.settings)
    syncer.start_syncing()
