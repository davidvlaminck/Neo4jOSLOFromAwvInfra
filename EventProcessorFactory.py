import importlib
import logging
from types import NoneType

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class EventProcessorFactory:
    processor_dict = {
        'NIEUWE_INSTALLATIE': 'NieuweInstallatieProcessor',
        'NIEUW_ONDERDEEL': 'NieuwOnderdeelProcessor',
        'ACTIEF_GEWIJZIGD': 'ActiefGewijzigdProcessor',
        'BESTEK_GEWIJZIGD': 'BestekGewijzigdProcessor',
        'BETROKKENE_RELATIES_GEWIJZIGD': 'BetrokkeneRelatiesGewijzigdProcessor',
        'COMMENTAAR_GEWIJZIGD': 'CommentaarGewijzigdProcessor',
        'EIGENSCHAPPEN_GEWIJZIGD': 'EigenschappenGewijzigdProcessor',
        'GEOMETRIE_GEWIJZIGD': 'GeometrieOrLocatieGewijzigdProcessor',
        'LOCATIE_GEWIJZIGD': 'GeometrieOrLocatieGewijzigdProcessor',
        'NAAM_GEWIJZIGD': 'NaamGewijzigdProcessor',
        'NAAMPAD_GEWIJZIGD': 'NaamGewijzigdProcessor',
        'PARENT_GEWIJZIGD': 'NaamGewijzigdProcessor',
        'RELATIES_GEWIJZIGD': 'AssetRelatiesGewijzigdProcessor',
        'SCHADEBEHEERDER_GEWIJZIGD': 'SchadebeheerderGewijzigdProcessor',
        'TOESTAND_GEWIJZIGD': 'ToestandGewijzigdProcessor',
        'TOEZICHT_GEWIJZIGD': 'ToezichtGewijzigdProcessor',
        'WEGLOCATIE_GEWIJZIGD': 'WeglocatieGewijzigdProcessor',
        'COMMUNICATIEAANSLUITING_GEWIJZIGD': NoneType,
        'DOCUMENTEN_GEWIJZIGD': NoneType,
        'ELEKTRICITEITSAANSLUITING_GEWIJZIGD': NoneType,
        'POSTIT_GEWIJZIGD': NoneType,
        'TOEGANG_GEWIJZIGD': NoneType,
        'VPLAN_GEWIJZIGD': NoneType
    }
    
    @classmethod
    def CreateEventProcessor(cls, event_type: str, tx_context: Transaction,
                             em_infra_importer: EMInfraImporter) -> SpecificEventProcessor:
        processor_type = cls.processor_dict.get(event_type)
        if processor_type is NoneType:
            pass
        elif processor_type is None:
            logging.error(f'events of type {event_type} are not supported.')
            raise NotImplementedError(f'events of type {event_type} are not supported.')
        else:
            processor_module = importlib.import_module(f'EventProcessors.{processor_type}')
            processor_type_class = getattr(processor_module, processor_type)
            return processor_type_class(tx_context, em_infra_importer)
