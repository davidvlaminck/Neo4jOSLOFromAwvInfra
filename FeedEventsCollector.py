from collections import namedtuple
from typing import NamedTuple

from EMInfraImporter import EMInfraImporter


class FeedEventsCollector:
    def __init__(self, emInfraImporter: EMInfraImporter):
        self.emInfraImporter = emInfraImporter

    def collect_events_from_feedproxy(self):
        pass

    def collect_starting_from_page(self, completed_page_number: int):
        event_dict = self.create_empty_event_dict()

        while True:
            page = self.emInfraImporter.get_event_from_page(completed_page_number + 1)
            entry_value = page['entries'][0]['content']['value']
            event_type = entry_value['event-type']
            event_uuids = entry_value['uuids']
            full_sync = 'event-id' not in entry_value
            event_dict[event_type].extend(event_uuids)

            if len(event_dict[event_type]) > 99:
                links = page['links']
                page_num = next(l for l in links if l['rel'] == 'self')['href'].split('/')[1]
                EventParams = namedtuple('EventParams', 'event_dict page_num full_sync')
                return EventParams(event_dict=event_dict, page_num=page_num, full_sync=full_sync)

    @staticmethod
    def create_empty_event_dict() -> {}:
        empty_dict = {}
        for event_type in ["ACTIEF_GEWIJZIGD", "BESTEK_GEWIJZIGD", "BETROKKENE_RELATIES_GEWIJZIGD", "COMMENTAAR_GEWIJZIGD",
                           "COMMUNICATIEAANSLUITING_GEWIJZIGD", "DOCUMENTEN_GEWIJZIGD", "EIGENSCHAPPEN_GEWIJZIGD",
                           "ELEKTRICITEITSAANSLUITING_GEWIJZIGD", "GEOMETRIE_GEWIJZIGD", "LOCATIE_GEWIJZIGD", "NAAM_GEWIJZIGD",
                           "NAAMPAD_GEWIJZIGD", "NIEUW_ONDERDEEL", "NIEUWE_INSTALLATIE", "PARENT_GEWIJZIGD", "POSTIT_GEWIJZIGD",
                           "RELATIES_GEWIJZIGD", "SCHADEBEHEERDER_GEWIJZIGD", "TOEGANG_GEWIJZIGD", "TOESTAND_GEWIJZIGD",
                           "TOEZICHT_GEWIJZIGD", "VPLAN_GEWIJZIGD"]:
            empty_dict[event_type] = []
        return empty_dict
