import logging
import time
import traceback

from AgentSyncer import AgentSyncer
from EMInfraImporter import EMInfraImporter
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError, BetrokkeneRelationNotCreatedError
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
            logging.info(f'starting a sync cycle, page: {str(completed_page_number + 1)}')
            eventsparams_to_process = self.events_collector.collect_starting_from_page(completed_page_number)

            total_events = sum(len(lists) for lists in eventsparams_to_process.event_dict.values())
            if total_events == 0:
                logging.info(f"The database is fully synced. Continuing keep up to date in 30 seconds")
                time.sleep(30)  # wait 30 seconds to prevent overloading API
                continue

            self.log_eventparams(eventsparams_to_process.event_dict)
            try:
                self.events_processor.process_events(eventsparams_to_process)
            except BetrokkeneRelationNotCreatedError:
                self.events_processor.tx_context.rollback()
                self.sync_all_agents()
            except Exception as exc:
                traceback.print_exception(exc)
                self.events_processor.tx_context.rollback()

            # agents syncen of na 24h

    @staticmethod
    def log_eventparams(event_dict):
        total = sum(len(events) for events in event_dict.values())
        logging.info(f'fetched {total} asset events to sync')
        for k, v in event_dict.items():
            if len(v) > 0:
                logging.info(f'number of events of type {k}: {len(v)}')

    def sync_all_agents(self):
        agentsyncer = AgentSyncer(emInfraImporter=self.eminfra_importer, neo4J_connector=self.connector)
        agentsyncer.sync_agents()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    request_handler = RequestHandler(cert_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                                     key_path=r'C:\resources\datamanager_eminfra_prd.awv.vlaanderen.be.key')
    eminfra_importer = EMInfraImporter(request_handler)
    syncer = Syncer(connector=connector, request_handler=request_handler, eminfra_importer=eminfra_importer)
    syncer.perform_syncing()
