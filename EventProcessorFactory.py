from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.ActiefGewijzigdProcessor import ActiefGewijzigdProcessor
from EventProcessors.BetrokkeneRelatiesGewijzigdProcessor import BetrokkeneRelatiesGewijzigdProcessor
from EventProcessors.CommentaarGewijzigdProcessor import CommentaarGewijzigdProcessor
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
        elif event_type == 'ACTIEF_GEWIJZIGD':
            return ActiefGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'BESTEK_GEWIJZIGD':
            pass
        elif event_type == 'BETROKKENE_RELATIES_GEWIJZIGD':
            return BetrokkeneRelatiesGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'COMMENTAAR_GEWIJZIGD':
            return CommentaarGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'COMMUNICATIEAANSLUITING_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'DOCUMENTEN_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'ELEKTRICITEITSAANSLUITING_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'GEOMETRIE_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'LOCATIE_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'NAAM_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'NAAMPAD_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'PARENT_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'POSTIT_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'RELATIES_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'SCHADEBEHEERDER_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'TOEGANG_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'TOESTAND_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'TOEZICHT_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'VPLAN_GEWIJZIGD':
            raise NotImplementedError
        else:
            pass
