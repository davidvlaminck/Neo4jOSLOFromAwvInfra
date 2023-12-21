import logging
from types import NoneType

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.ActiefGewijzigdProcessor import ActiefGewijzigdProcessor
from EventProcessors.AssetRelatiesGewijzigdProcessor import AssetRelatiesGewijzigdProcessor
from EventProcessors.BestekGewijzigdProcessor import BestekGewijzigdProcessor
from EventProcessors.BetrokkeneRelatiesGewijzigdProcessor import BetrokkeneRelatiesGewijzigdProcessor
from EventProcessors.CommentaarGewijzigdProcessor import CommentaarGewijzigdProcessor
from EventProcessors.EigenschappenGewijzigdProcessor import EigenschappenGewijzigdProcessor
from EventProcessors.GeometrieOrLocatieGewijzigdProcessor import GeometrieOrLocatieGewijzigdProcessor
from EventProcessors.NaamGewijzigdProcessor import NaamGewijzigdProcessor
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor
from EventProcessors.NieuweInstallatieProcessor import NieuweInstallatieProcessor
from EventProcessors.SchadebeheerderGewijzigdProcessor import SchadebeheerderGewijzigdProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor
from EventProcessors.ToestandGewijzigdProcessor import ToestandGewijzigdProcessor
from EventProcessors.ToezichtGewijzigdProcessor import ToezichtGewijzigdProcessor
from EventProcessors.WegLocatieGewijzigdProcessor import WeglocatieGewijzigdProcessor


class EventProcessorFactory:
    processor_dict = {
        'NIEUWE_INSTALLATIE': NieuweInstallatieProcessor,
        'NIEUW_ONDERDEEL': NieuwOnderdeelProcessor,
        'ACTIEF_GEWIJZIGD': ActiefGewijzigdProcessor,
        'BESTEK_GEWIJZIGD': BestekGewijzigdProcessor,
        'BETROKKENE_RELATIES_GEWIJZIGD': BetrokkeneRelatiesGewijzigdProcessor,
        'COMMENTAAR_GEWIJZIGD': CommentaarGewijzigdProcessor,
        'EIGENSCHAPPEN_GEWIJZIGD': EigenschappenGewijzigdProcessor,
        'GEOMETRIE_GEWIJZIGD': GeometrieOrLocatieGewijzigdProcessor,
        'LOCATIE_GEWIJZIGD': GeometrieOrLocatieGewijzigdProcessor,
        'NAAM_GEWIJZIGD': NaamGewijzigdProcessor,
        'NAAMPAD_GEWIJZIGD': NaamGewijzigdProcessor,
        'PARENT_GEWIJZIGD': NaamGewijzigdProcessor,
        'RELATIES_GEWIJZIGD': AssetRelatiesGewijzigdProcessor,
        'SCHADEBEHEERDER_GEWIJZIGD': SchadebeheerderGewijzigdProcessor,
        'TOESTAND_GEWIJZIGD': ToestandGewijzigdProcessor,
        'TOEZICHT_GEWIJZIGD': ToezichtGewijzigdProcessor,
        'WEGLOCATIE_GEWIJZIGD': WeglocatieGewijzigdProcessor,
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
            return processor_type(tx_context, em_infra_importer)

