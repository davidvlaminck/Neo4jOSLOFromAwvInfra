import json
import logging
from pathlib import Path

from AbstractRequester import AbstractRequester
from EMInfraImporter import EMInfraImporter
from Enums import AuthType, Environment
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

    connector = Neo4JConnector(uri="bolt://localhost:7687", user="neo4j", password="neo4jadmin", database='neo4j')
    settings_path = Path('/home/davidlinux/Documents/AWV/resources/settings_neo4jmodelcreator.json')
    # settings_path = Path('C:\\resources\\settings_neo4jmodelcreator.json')

    with open(settings_path) as settings_file:
        settings = json.load(settings_file)

    requester = RequesterFactory.create_requester(settings=settings, auth_type=AuthType.JWT, env=Environment.PRD)

    eminfra_importer = EMInfraImporter(requester)
    syncer = Syncer(connector=connector, requester=requester, eminfra_importer=eminfra_importer, settings=settings)
    syncer.start_syncing()
