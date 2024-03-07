import logging

from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler
from RequesterFactory import RequesterFactory
from SettingsManager import SettingsManager
from Syncer import Syncer
from decouple import Config, RepositoryEnv

if __name__ == '__main__':
    # Settings
    logging.basicConfig(level=logging.INFO)
    config = Config(RepositoryEnv(r"C:\Users\devosar\PycharmProjects\Intelligent Incident Detection (IID)\utils\.env"))

    # Set up connection to Neo4j instance (DBMS)
    username = config('username_neo4j', default='')  # not just username because this is predefined variable, see .env
    password = config('password_neo4j', default='')
    connector = Neo4JConnector(uri="bolt://localhost:7687", user=username, password=password)



    # Syncing settings
    settings_manager = SettingsManager(settings_path='.\\settings_neo4jmodelcreator.json')
    requester = RequesterFactory.create_requester(settings=settings_manager.settings, auth_type='JWT', env='prd')
    request_handler = RequestHandler(requester)

    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer, settings=settings_manager.settings)
    syncer.start_syncing()
