from collections import namedtuple

from EMInfraImporter import EMInfraImporter

EventParams = namedtuple('EventParams', 'event_dict page_num event_id')


class FeedEventsCollector:
    def __init__(self, emInfraImporter: EMInfraImporter):
        self.emInfraImporter = emInfraImporter

    def collect_starting_from_page(self, completed_page_number: int, completed_event_id: int, page_size: int) -> EventParams:
        event_dict = self.create_empty_event_dict()
        while True:
            page = self.emInfraImporter.get_events_from_page(page_num=completed_page_number, page_size=page_size)
            stop_after_this_page = False
            last_event_id = -1

            entries = sorted(page['entries'], key=lambda p: int(p['content']['value']['event-id']))

            for entry in entries:
                entry_value = entry['content']['value']
                event_id = entry_value['event-id']
                if event_id <= completed_event_id:
                    continue
                event_type = entry_value['event-type']
                event_uuids = entry_value['uuids']
                event_dict[event_type].update(event_uuids)

                if len(event_dict[event_type]) >= 50:
                    stop_after_this_page = True

                if stop_after_this_page:
                    last_event_id = event_id

            if stop_after_this_page:
                links = page['links']
                page_num = next(link for link in links if link['rel'] == 'self')['href'].split('/')[1]

                return EventParams(event_dict=event_dict, page_num=page_num, event_id=last_event_id)

            completed_page_number += 1

    @staticmethod
    def create_empty_event_dict() -> {}:
        empty_dict = {}
        for event_type in ["ACTIEF_GEWIJZIGD", "BESTEK_GEWIJZIGD", "BETROKKENE_RELATIES_GEWIJZIGD", "COMMENTAAR_GEWIJZIGD",
                           "COMMUNICATIEAANSLUITING_GEWIJZIGD", "DOCUMENTEN_GEWIJZIGD", "EIGENSCHAPPEN_GEWIJZIGD",
                           "ELEKTRICITEITSAANSLUITING_GEWIJZIGD", "GEOMETRIE_GEWIJZIGD", "LOCATIE_GEWIJZIGD", "NAAM_GEWIJZIGD",
                           "NAAMPAD_GEWIJZIGD", "NIEUW_ONDERDEEL", "NIEUWE_INSTALLATIE", "PARENT_GEWIJZIGD", "POSTIT_GEWIJZIGD",
                           "RELATIES_GEWIJZIGD", "SCHADEBEHEERDER_GEWIJZIGD", "TOEGANG_GEWIJZIGD", "TOESTAND_GEWIJZIGD",
                           "TOEZICHT_GEWIJZIGD", "VPLAN_GEWIJZIGD"]:
            empty_dict[event_type] = set()
        return empty_dict
