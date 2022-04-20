from copy import copy
from unittest import TestCase, mock

from EMInfraImporter import EMInfraImporter


class EMInfraImporterTests(TestCase):
    @staticmethod
    def get_single_relatie():
        return copy({
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing",
            "@id": "https://data.awvvlaanderen.be/id/assetrelatie/00000000-0001-0002-0000-000000000001-b25kZXJkZWVsI0JldmVzdGlnaW5n",
            "RelatieObject.bron": {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": "https://data.awvvlaanderen.be/id/asset/00000000-0000-0000-0000-000000000001-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.doel": {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                "@id": "https://data.awvvlaanderen.be/id/asset/00000000-0000-0000-0000-000000000002-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Sturing",
            "AIMDBStatus.isActief": True,
            "RelatieObject.bronAssetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": "00000000-0000-0000-0000-000000000001-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.doelAssetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": "00000000-0000-0000-0000-000000000002-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "RelatieObject.assetId": {
                "DtcIdentificator.identificator": "00000000-0001-0002-0000-000000000001-b25kZXJkZWVsI0JldmVzdGlnaW5n",
                "DtcIdentificator.toegekendDoor": "AWV"
            }
        })

    def test_get_distinct_set_from_list_of_relations_simple_tests(self):
        relatie1 = self.get_single_relatie()
        relatie2 = self.get_single_relatie()
        assetId2 = '00000000-0002-0003-0000-000000000002-b25kZXJkZWVsI0JldmVzdGlnaW5n'
        relatie2["@id"] = f'https://data.awvvlaanderen.be/id/assetrelatie/{assetId2}'
        relatie2["RelatieObject.assetId"]["DtcIdentificator.identificator"] = assetId2

        with self.subTest('empty list'):
            result = EMInfraImporter.get_distinct_set_from_list_of_relations([])
            self.assertListEqual([], result)

        with self.subTest('single relation in list'):
            result = EMInfraImporter.get_distinct_set_from_list_of_relations([relatie1])
            self.assertListEqual([relatie1], result)

        with self.subTest('two nonidentical relations in list'):
            result = EMInfraImporter.get_distinct_set_from_list_of_relations([relatie1, relatie2])
            self.assertListEqual([relatie1, relatie2], result)

    def test_get_distinct_set_from_list_of_relations_two_identical_relations(self):
        relatie1 = self.get_single_relatie()
        relatie2 = self.get_single_relatie()

        result = EMInfraImporter.get_distinct_set_from_list_of_relations([relatie1, relatie2])
        self.assertListEqual([relatie1], result)



