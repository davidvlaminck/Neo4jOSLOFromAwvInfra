import logging
import time
from unittest import TestCase, mock

from EMInfraImporter import EMInfraImporter
from EventProcessors.NieuwAssetProcessor import NieuwAssetProcessor
from FeedEventsCollector import EventParams
from FeedEventsProcessor import FeedEventsProcessor
from Neo4JConnector import Neo4JConnector
from UnitTests.ResponseDouble import ResponseDouble


class EventProcessorsTests(TestCase):
    """These tests require a running instance of neo4J, defined in the setUp method"""

    def setUp(self) -> None:
        logging.basicConfig(level=logging.INFO)
        self.connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
        self.feedEventsProcessor = FeedEventsProcessor(neo4J_connector=self.connector, emInfraImporter=mock.Mock())
        self.tx_context = self.connector.start_transaction()

    def tearDown(self) -> None:
        self.tx_context.rollback()
        self.setUp()

    def create_uuid_from_int(self, i: int = 0):
        i_str = str(i)
        if i < 10:
            i_str = '0' + i_str
        return '00000000-0000-0000-0000-0000000000' + i_str

    def create_assetrelatie_in_double(self, i: int = 0):
        i_str = str(i)
        if i < 10:
            i_str = '0' + i_str
        j = i + 1
        j_str = str(j)
        if j < 10:
            j_str = '0' + j_str
        k = i + 2
        k_str = str(k)
        if k < 10:
            k_str = '0' + k_str

        relaties = []

        relatie_uuid_j = f'00000000-00{i_str}-00{j_str}-0000-000000000000'
        relatie_uuid_k = f'00000000-00{i_str}-00{k_str}-0000-000000000000'

        relatie_i_j = {
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing",
            "@id": f"https://data.awvvlaanderen.be/id/assetrelatie/{relatie_uuid_j}-b25kZXJkZWVsI0JldmVzdGlnaW5n",
            "RelatieObject.bron": {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": f"https://data.awvvlaanderen.be/id/asset/00000000-0000-0000-0000-0000000000{i_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.doel": {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": f"https://data.awvvlaanderen.be/id/asset/00000000-0000-0000-0000-0000000000{j_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing",
            "AIMDBStatus.isActief": True,
            "RelatieObject.bronAssetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": f"00000000-0000-0000-0000-0000000000{i_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.doelAssetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": f"00000000-0000-0000-0000-0000000000{j_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.assetId": {
                "DtcIdentificator.identificator": f"{relatie_uuid_j}-b25kZXJkZWVsI0JldmVzdGlnaW5n",
                "DtcIdentificator.toegekendDoor": "AWV"
            }
        }
        relatie_i_k = {
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing",
            "@id": f"https://data.awvvlaanderen.be/id/assetrelatie/{relatie_uuid_k}-b25kZXJkZWVsI0JldmVzdGlnaW5n",
            "RelatieObject.bron": {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": f"https://data.awvvlaanderen.be/id/asset/00000000-0000-0000-0000-0000000000{i_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.doel": {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": f"https://data.awvvlaanderen.be/id/asset/00000000-0000-0000-0000-0000000000{k_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing",
            "AIMDBStatus.isActief": True,
            "RelatieObject.bronAssetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": f"00000000-0000-0000-0000-0000000000{i_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.doelAssetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": f"00000000-0000-0000-0000-0000000000{k_str}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.assetId": {
                "DtcIdentificator.identificator": f"{relatie_uuid_k}-b25kZXJkZWVsI0JldmVzdGlnaW5n",
                "DtcIdentificator.toegekendDoor": "AWV"
            }
        }

        if 'otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + i_str not in ResponseDouble.endpoint_orig:
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + i_str] = []
        if 'otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + j_str not in ResponseDouble.endpoint_orig:
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + j_str] = []
        if 'otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + k_str not in ResponseDouble.endpoint_orig:
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + k_str] = []

        if j < 90:
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + i_str].append(
                relatie_i_j)
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + j_str].append(
                relatie_i_j)
        if k < 90:
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + i_str].append(
                relatie_i_k)
            ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + k_str].append(
                relatie_i_k)
        ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + i_str] = \
            EMInfraImporter.get_distinct_set_from_list_of_relations(ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + i_str])
        ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + j_str] = \
            EMInfraImporter.get_distinct_set_from_list_of_relations(ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + j_str])
        ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + k_str] = \
            EMInfraImporter.get_distinct_set_from_list_of_relations(ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + '00000000-0000-0000-0000-0000000000' + k_str])

    def create_assets_in_double(self):
        for i in range(90):
            uuid = self.create_uuid_from_int(i)
            ResponseDouble.endpoint_orig['otl/assets/search/' + uuid] = [{
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": f"https://data.awvvlaanderen.be/id/asset/{uuid}-b25kZXJkZWVsI05ldHdlcmtwb29ydA",
                "AIMObject.assetId": {
                    "DtcIdentificator.toegekendDoor": "AWV",
                    "DtcIdentificator.identificator": f"{uuid}-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "AIMObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
            }]
            self.create_assetrelatie_in_double(i)

    def test_assetrelaties_gewijzigd(self):
        self.setUp()

        self.create_assets_in_double()

        # create test assets
        uuids = []
        for i in range(90):
            uuid = self.create_uuid_from_int(i)
            uuids.append(uuid)

        asset_processor = NieuwAssetProcessor()
        asset_processor.tx_context = self.tx_context
        for uuid in uuids:
            asset_processor.create_asset_from_jsonLd_dict(ResponseDouble.endpoint_orig['otl/assets/search/' + uuid][0])

        uuids = uuids[0:3]

        # create a fake EMinfra importer
        emInfraImporter = mock.Mock()

        def import_assetrelaties_from_webservice_by_assetuuids_fixed(asset_uuids):
            list = []
            for uuid in asset_uuids:
                list.extend(ResponseDouble.endpoint_orig['otl/assetrelaties/search/' + uuid])

            return EMInfraImporter.get_distinct_set_from_list_of_relations(list)

        emInfraImporter.import_assetrelaties_from_webservice_by_assetuuids = import_assetrelaties_from_webservice_by_assetuuids_fixed

        # test before change
        query = 'UNWIND $params as uuids MATCH (Asset {uuid: uuids})-[r]-(Asset) return count(r)'
        result_before_event = self.tx_context.run(query, params=uuids).single()[0]
        self.assertEqual(0, result_before_event)

        # self.assertGreater(0, len(emInfraImporter.import_assetrelaties_from_webservice_by_assetuuids(uuids)))

        # set up events to process
        eventsparams_to_process = self.create_events(uuids)

        # make the change
        # process events
        processor = FeedEventsProcessor(self.connector, emInfraImporter)

        start = time.time()
        processor.process_events_by_event_params(eventsparams_to_process, self.tx_context)
        end = time.time()

        print("time taken :" + str(round(end - start, 2)))

        # test after change
        result_after_event = self.tx_context.run(query, params=uuids).single()[0]
        self.assertEqual(355, result_after_event)

        self.tearDown()

    def create_events(self, assetuuids):
        eventsparams_to_process = EventParams(event_dict={
            'RELATIES_GEWIJZIGD': set(assetuuids),
        }, page_num='12427', event_id=5839578)
        return eventsparams_to_process
