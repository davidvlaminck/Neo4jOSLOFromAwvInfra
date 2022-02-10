import time

from EMInfraImporter import EMInfraImporter
from FeedEventsCollector import FeedEventsCollector
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from RequestHandler import RequestHandler


class Syncer:
    def __init__(self, connector: Neo4JConnector, request_handler: RequestHandler, eminfra_importer: EMInfraImporter):
        self.connector = connector
        self.request_handler = request_handler
        self.eminfra_importer = eminfra_importer
        self.events_collector = FeedEventsCollector(eminfra_importer)
        self.events_processor = FeedEventsProcessor(connector, eminfra_importer)

    def perform_syncing(self):
        while True:
            completed_page_number = self.connector.get_page_by_get_or_create_params()
            eventsparams_to_process = self.events_collector.collect_starting_from_page(completed_page_number)
            self.events_processor.process_events(eventsparams_to_process)
            time.sleep(30) # wait 30 seconds to prevent overloading API

if __name__ == '__main__':
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    request_handler = RequestHandler(cert_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                                     key_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.key')
    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer)
    syncer.perform_syncing()
