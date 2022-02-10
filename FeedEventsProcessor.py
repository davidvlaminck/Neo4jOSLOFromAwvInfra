from EMInfraImporter import EMInfraImporter
from EventProcessorFactory import EventProcessorFactory
from Neo4JConnector import Neo4JConnector


class FeedEventsProcessor:
    def __init__(self, neo4J_connector: Neo4JConnector, emInfraImporter: EMInfraImporter):
        self.neo4J_connector = neo4J_connector
        self.emInfraImporter = emInfraImporter

    def process_events(self, event_params: ()):
        event_dict = event_params.event_dict

        tx_context = self.neo4J_connector.start_transaction()

        # make sure events NIEUW_ONDERDEEL and NIEUWE_INSTALLATIE are processed before any others
        if len(event_dict["NIEUW_ONDERDEEL"]) > 0:
            event_processor = self.create_processor("NIEUW_ONDERDEEL", tx_context)
            event_processor.process(event_dict["NIEUW_ONDERDEEL"], event_params.full_sync)
        if len(event_dict["NIEUWE_INSTALLATIE"]) > 0:
            event_processor = self.create_processor("NIEUWE_INSTALLATIE", tx_context)
            event_processor.process(event_dict["NIEUWE_INSTALLATIE"], event_params.full_sync)
        for event_type, uuids in event_dict.items():
            if event_type in ["NIEUW_ONDERDEEL", "NIEUWE_INSTALLATIE"] or len(uuids) == 0:
                continue
            raise NotImplementedError
            event_processor = self.create_processor(event_type, tx_context)
            event_processor.process(uuids)
        pass

        page_num = event_params.page_num
        self.neo4J_connector.update_params(tx_context, page_num)
        self.neo4J_connector.commit_transaction(tx_context)

    def create_processor(self, event_type, tx_context):
        event_processor = EventProcessorFactory.CreateEventProcessor(event_type=event_type, tx_context=tx_context,
                                                                     emInfraImporter=self.emInfraImporter)
        return event_processor
