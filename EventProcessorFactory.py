from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.ActiefGewijzigdProcessor import ActiefGewijzigdProcessor
from EventProcessors.AssetRelatiesGewijzigdProcessor import AssetRelatiesGewijzigdProcessor
from EventProcessors.BetrokkeneRelatiesGewijzigdProcessor import BetrokkeneRelatiesGewijzigdProcessor
from EventProcessors.CommentaarGewijzigdProcessor import CommentaarGewijzigdProcessor
from EventProcessors.GeometrieOrLocatieGewijzigdProcessor import GeometrieOrLocatieGewijzigdProcessor
from EventProcessors.NaamGewijzigdProcessor import NaamGewijzigdProcessor
from EventProcessors.NieuwOnderdeelProcessor import NieuwOnderdeelProcessor
from EventProcessors.NieuweInstallatieProcessor import NieuweInstallatieProcessor
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor
from EventProcessors.ToestandGewijzigdProcessor import ToestandGewijzigdProcessor


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
            pass
        elif event_type == 'DOCUMENTEN_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'ELEKTRICITEITSAANSLUITING_GEWIJZIGD':
            pass
        elif event_type == 'GEOMETRIE_GEWIJZIGD' or event_type == 'LOCATIE_GEWIJZIGD':
            return GeometrieOrLocatieGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'NAAM_GEWIJZIGD' or event_type == 'NAAMPAD_GEWIJZIGD' or event_type == 'PARENT_GEWIJZIGD':
            return NaamGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'POSTIT_GEWIJZIGD':
            pass
        elif event_type == 'RELATIES_GEWIJZIGD':
            return AssetRelatiesGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'SCHADEBEHEERDER_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'TOEGANG_GEWIJZIGD':
            pass
        elif event_type == 'TOESTAND_GEWIJZIGD':
            return ToestandGewijzigdProcessor(tx_context, emInfraImporter)
        elif event_type == 'TOEZICHT_GEWIJZIGD':
            raise NotImplementedError
        elif event_type == 'VPLAN_GEWIJZIGD':
            pass
        else:
            raise NotImplementedError
