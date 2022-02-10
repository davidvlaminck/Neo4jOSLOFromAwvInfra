from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor
from EventProcessors.NieuweInstallatieProcessor import NieuweInstallatieProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class EventProcessorFactory:
    @classmethod
    def CreateEventProcessor(cls, event_type: str, tx_context: Transaction,
                             emInfraImporter: EMInfraImporter) -> SpecificEventProcessor:
        if event_type == 'NIEUWE_INSTALLATIE':
            return NieuweInstallatieProcessor(tx_context, emInfraImporter)
        elif event_type == 'NIEUW_ONDERDEEL':
            return NieuwOnderdeelProcessor(tx_context, emInfraImporter)
        else:
            pass
