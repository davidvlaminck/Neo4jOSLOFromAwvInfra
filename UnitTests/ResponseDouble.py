class ResponseDouble:
    mogelijke_events = ["ACTIEF_GEWIJZIGD", "BESTEK_GEWIJZIGD", "BETROKKENE_RELATIES_GEWIJZIGD", "COMMENTAAR_GEWIJZIGD",
                        "COMMUNICATIEAANSLUITING_GEWIJZIGD", "DOCUMENTEN_GEWIJZIGD", "EIGENSCHAPPEN_GEWIJZIGD",
                        "ELEKTRICITEITSAANSLUITING_GEWIJZIGD", "GEOMETRIE_GEWIJZIGD", "LOCATIE_GEWIJZIGD", "NAAM_GEWIJZIGD",
                        "NAAMPAD_GEWIJZIGD", "NIEUW_ONDERDEEL", "NIEUWE_INSTALLATIE", "PARENT_GEWIJZIGD", "POSTIT_GEWIJZIGD",
                        "RELATIES_GEWIJZIGD", "SCHADEBEHEERDER_GEWIJZIGD", "TOEGANG_GEWIJZIGD", "TOESTAND_GEWIJZIGD",
                        "TOEZICHT_GEWIJZIGD", "VPLAN_GEWIJZIGD", ""]
    endpoint_orig = {
        'otl/assets/search/bbac4a9a-905a-4991-bafa-43126fb5db10': [{
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkelement",
            "@id": "https://data.awvvlaanderen.be/id/asset/bbac4a9a-905a-4991-bafa-43126fb5db10-b25kZXJkZWVsI05ldHdlcmtlbGVtZW50",
            "Netwerkelement.beschrijvingFabrikant": "AM1+",
            "AIMObject.notitie": "",
            "Netwerkelement.softwareVersie": "SCA402H  ",
            "Netwerkelement.merk": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkMerk/NOKIA",
            "AIMDBStatus.isActief": True,
            "AIMNaamObject.naam": "BELFLANTLa",
            "Netwerkelement.modelnaam": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkelemModelnaam/AM1+",
            "Netwerkelement.nSAPAddress": "143900008000000000000000000200601D33FA3101",
            "Netwerkelement.ipAddressBeheer": "n/a",
            "Netwerkelement.serienummer": "04R204151849",
            "AIMObject.assetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": "bbac4a9a-905a-4991-bafa-43126fb5db10-b25kZXJkZWVsI05ldHdlcmtlbGVtZW50"
            },
            "AIMObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkelement",
            "AIMToestand.toestand": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/in-gebruik",
            "Netwerkelement.gebruik": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkelemGebruik/sdh"
        }],
        'otl/assets/search/c531aad8-e7c3-49f6-8c0d-c228a0c17c02': [{
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Link",
            "@id": "https://data.awvvlaanderen.be/id/asset/c531aad8-e7c3-49f6-8c0d-c228a0c17c02-aW5zdGFsbGF0aWUjTGluaw",
            "AIMObject.notitie": "",
            "AIMDBStatus.isActief": True,
            "AIMObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Link",
            "NaampadObject.naampad": "OTN.LINK/Link_498",
            "AIMNaamObject.naam": "Link_498",
            "AIMObject.assetId": {
                "DtcIdentificator.identificator": "c531aad8-e7c3-49f6-8c0d-c228a0c17c02-aW5zdGFsbGF0aWUjTGluaw",
                "DtcIdentificator.toegekendDoor": "AWV"
            },
            "AIMToestand.toestand": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/in-gebruik",
            "Link.geleidingsgroepTnummer": 0
        }],
        'otl/assets/search/000a35d5-c4a5-4a36-8620-62c99e053ba0': [{
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
            "@id": "https://data.awvvlaanderen.be/id/asset/000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA",
            "Netwerkpoort.config": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkpoortConfig/STM-1",
            "Netwerkpoort.merk": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkMerk/NOKIA",
            "loc:Locatie.puntlocatie": "",
            "AIMDBStatus.isActief": True,
            "Netwerkpoort.nNILANCapaciteit": 155,
            "AIMObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
            "Netwerkpoort.golflengte": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkpoortGolflengte/NULL",
            "AIMObject.assetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": "000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "AIMObject.notitie": "",
            "loc:Locatie.omschrijving": "",
            "Netwerkpoort.technologie": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkTechnologie/SDH",
            "AIMToestand.toestand": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/in-gebruik",
            "loc:Locatie.geometrie": "",
            "AIMNaamObject.naam": "BELFLANTLa_LS2.1"
        }],
        'otl/assets/search/00000453-56ce-4f8b-af44-960df526cb30': [{
            "@type": "https://lgc.data.wegenenverkeer.be/ns/installatie#Kast",
            "@id": "https://data.awvvlaanderen.be/id/asset/00000453-56ce-4f8b-af44-960df526cb30-bGdjOmluc3RhbGxhdGllI0thc3Q",
            "NaampadObject.naampad": "057A5/KAST",
            "AIMObject.notitie": "",
            "AIMObject.typeURI": "https://lgc.data.wegenenverkeer.be/ns/installatie#Kast",
            "AIMDBStatus.isActief": True,
            "AIMObject.assetId": {
                "DtcIdentificator.identificator": "00000453-56ce-4f8b-af44-960df526cb30-bGdjOmluc3RhbGxhdGllI0thc3Q",
                "DtcIdentificator.toegekendDoor": "AWV"
            },
            "tz:Toezicht.toezichtgroep": {
                "tz:DtcToezichtGroep.referentie": "AWV_EW_AN",
                "tz:DtcToezichtGroep.naam": "AWV_EW_AN"
            },
            "loc:Locatie.puntlocatie": {
                "loc:DtcPuntlocatie.weglocatie": {
                    "loc:DtcWeglocatie.referentiepaalAfstand": 45,
                    "loc:DtcWeglocatie.ident2": "N156",
                    "loc:DtcWeglocatie.ident8": "N1560001",
                    "loc:DtcWeglocatie.gemeente": "Geel",
                    "loc:DtcWeglocatie.straatnaam": "Amocolaan",
                    "loc:DtcWeglocatie.referentiepaalOpschrift": 10.8
                },
                "loc:3Dpunt.puntgeometrie": {
                    "loc:DtcCoord.lambert72": {
                        "loc:DtcCoordLambert72.xcoordinaat": 192721.4,
                        "loc:DtcCoordLambert72.ycoordinaat": 201119.2,
                        "loc:DtcCoordLambert72.zcoordinaat": 0
                    }
                },
                "loc:DtcPuntlocatie.adres": {
                    "loc:DtcAdres.postcode": "2440",
                    "loc:DtcAdres.bus": "",
                    "loc:DtcAdres.straat": "Oosterloseweg",
                    "loc:DtcAdres.gemeente": "Geel",
                    "loc:DtcAdres.provincie": "Antwerpen",
                    "loc:DtcAdres.nummer": "36"
                },
                "loc:DtcPuntlocatie.precisie": "https://loc.data.wegenenverkeer.be/id/concept/KlLocatiePrecisie/meter",
                "loc:DtcPuntlocatie.bron": "https://loc.data.wegenenverkeer.be/id/concept/KlLocatieBron/manueel"
            },
            "AIMNaamObject.naam": "KAST",
            "tz:Toezicht.toezichter": {
                "tz:DtcToezichter.email": "niels.vanasch@mow.vlaanderen.be",
                "tz:DtcToezichter.voornaam": "Niels",
                "tz:DtcToezichter.naam": "Van Asch",
                "tz:DtcToezichter.gebruikersnaam": "vanascni"
            },
            "loc:Locatie.omschrijving": "",
            "tz:Schadebeheerder.schadebeheerder": {
                "tz:DtcBeheerder.naam": "District Geel",
                "tz:DtcBeheerder.referentie": "114"
            },
            "AIMToestand.toestand": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/in-gebruik",
            "loc:Locatie.geometrie": ""
        }],
        'otl/betrokkenerelaties/search/000a35d5-c4a5-4a36-8620-62c99e053ba0': [
            {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBetrokkene",
                "@id": "https://data.awvvlaanderen.be/id/assetrelatie/e48b9474-babd-450a-964f-5b4a8902fb4c-b25kZXJkZWVsI0hlZWZ0QmV0cm9ra2VuZQ",
                "RelatieObject.bron": {
                    "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                    "@id": "https://data.awvvlaanderen.be/id/asset/000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "RelatieObject.doel": {
                    "@type": "http://purl.org/dc/terms/Agent",
                    "@id": "https://data.awvvlaanderen.be/id/asset/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0-cHVybDpBZ2VudA"
                },
                "HeeftBetrokkene.specifiekeContactinfo": [],
                "AIMDBStatus.isActief": True,
                "HeeftBetrokkene.rol": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetrokkenheidRol/toezichter"
            }
        ],
        'otl/assetrelaties/search/000a35d5-c4a5-4a36-8620-62c99e053ba0': [
            {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HoortBij",
                "@id": "https://data.awvvlaanderen.be/id/assetrelatie/1ce81d00-43c8-438f-893f-3468f56b218a-b25kZXJkZWVsI0hvb3J0Qmlq",
                "RelatieObject.bron": {
                    "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                    "@id": "https://data.awvvlaanderen.be/id/asset/000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "RelatieObject.doel": {
                    "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/installatie#Link",
                    "@id": "https://data.awvvlaanderen.be/id/asset/c531aad8-e7c3-49f6-8c0d-c228a0c17c02-aW5zdGFsbGF0aWUjTGluaw"
                },
                "RelatieObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HoortBij",
                "RelatieObject.doelAssetId": {
                    "DtcIdentificator.identificator": "c531aad8-e7c3-49f6-8c0d-c228a0c17c02-aW5zdGFsbGF0aWUjTGluaw",
                    "DtcIdentificator.toegekendDoor": "AWV"
                },
                "AIMDBStatus.isActief": True,
                "RelatieObject.bronAssetId": {
                    "DtcIdentificator.toegekendDoor": "AWV",
                    "DtcIdentificator.identificator": "000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "RelatieObject.assetId": {
                    "DtcIdentificator.identificator": "1ce81d00-43c8-438f-893f-3468f56b218a-b25kZXJkZWVsI0hvb3J0Qmlq",
                    "DtcIdentificator.toegekendDoor": "AWV"
                }
            }
        ],
        'otl/agents/search/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0': [{
            "@type": "http://purl.org/dc/terms/Agent",
            "@id": "https://data.awvvlaanderen.be/id/asset/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0-cHVybDpBZ2VudA",
            "purl:Agent.naam": "Steve Desmadryl",
            "purl:Agent.contactinfo": []
        }],
        'otl/agents/search/35de1da1-8ef3-45bf-bf91-cdb23e0889cc': [{
            "@type": "http://purl.org/dc/terms/Agent",
            "@id": "https://data.awvvlaanderen.be/id/asset/35de1da1-8ef3-45bf-bf91-cdb23e0889cc-cHVybDpBZ2VudA",
            "purl:Agent.contactinfo": [],
            "purl:Agent.naam": "EMT_TELE"
        }]
    }
    endpoint_changed = {
        'otl/assets/search/000a35d5-c4a5-4a36-8620-62c99e053ba0': [{
            "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
            "@id": "https://data.awvvlaanderen.be/id/asset/000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA",
            "Netwerkpoort.config": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkpoortConfig/STM-1",
            "Netwerkpoort.merk": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkMerk/NOKIA",
            "loc:Locatie.puntlocatie": "",
            "AIMDBStatus.isActief": False,
            "Netwerkpoort.nNILANCapaciteit": 200,
            "AIMObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
            "Netwerkpoort.golflengte": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkpoortGolflengte/NULL",
            "AIMObject.assetId": {
                "DtcIdentificator.toegekendDoor": "AWV",
                "DtcIdentificator.identificator": "000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
            },
            "AIMObject.notitie": "aangepaste notitie",
            "loc:Locatie.omschrijving": "",
            "Netwerkpoort.technologie": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlNetwerkTechnologie/SDH",
            "AIMToestand.toestand": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/verwijderd",
            "loc:Locatie.geometrie": "",
            "AIMNaamObject.naam": "nieuwe_naam"
        }],
        'otl/assets/search/00000453-56ce-4f8b-af44-960df526cb30': [{
            "@type": "https://lgc.data.wegenenverkeer.be/ns/installatie#Kast",
            "@id": "https://data.awvvlaanderen.be/id/asset/00000453-56ce-4f8b-af44-960df526cb30-bGdjOmluc3RhbGxhdGllI0thc3Q",
            "NaampadObject.naampad": "057A5/057A5.K",
            "AIMObject.notitie": "",
            "AIMObject.typeURI": "https://lgc.data.wegenenverkeer.be/ns/installatie#Kast",
            "AIMDBStatus.isActief": True,
            "AIMObject.assetId": {
                "DtcIdentificator.identificator": "00000453-56ce-4f8b-af44-960df526cb30-bGdjOmluc3RhbGxhdGllI0thc3Q",
                "DtcIdentificator.toegekendDoor": "AWV"
            },
            "tz:Toezicht.toezichtgroep": {
                "tz:DtcToezichtGroep.referentie": "EMT_TELE",
                "tz:DtcToezichtGroep.naam": "EMT_TELE"
            },
            "loc:Locatie.puntlocatie": {
                "loc:DtcPuntlocatie.weglocatie": {
                    "loc:DtcWeglocatie.referentiepaalAfstand": 45,
                    "loc:DtcWeglocatie.ident2": "N156",
                    "loc:DtcWeglocatie.ident8": "N1560001",
                    "loc:DtcWeglocatie.gemeente": "Antwerpen",
                    "loc:DtcWeglocatie.straatnaam": "Amocolaan",
                    "loc:DtcWeglocatie.referentiepaalOpschrift": 10.8
                },
                "loc:3Dpunt.puntgeometrie": {
                    "loc:DtcCoord.lambert72": {
                        "loc:DtcCoordLambert72.xcoordinaat": 150000,
                        "loc:DtcCoordLambert72.ycoordinaat": 250000,
                        "loc:DtcCoordLambert72.zcoordinaat": 0
                    }
                },
                "loc:DtcPuntlocatie.adres": {
                    "loc:DtcAdres.postcode": "2440",
                    "loc:DtcAdres.bus": "",
                    "loc:DtcAdres.straat": "Oosterloseweg",
                    "loc:DtcAdres.gemeente": "Geel",
                    "loc:DtcAdres.provincie": "Antwerpen",
                    "loc:DtcAdres.nummer": "36"
                },
                "loc:DtcPuntlocatie.precisie": "https://loc.data.wegenenverkeer.be/id/concept/KlLocatiePrecisie/meter",
                "loc:DtcPuntlocatie.bron": "https://loc.data.wegenenverkeer.be/id/concept/KlLocatieBron/manueel"
            },
            "AIMNaamObject.naam": "057A5.K",
            "tz:Toezicht.toezichter": {
                "tz:DtcToezichter.email": "niels.vanasch@mow.vlaanderen.be",
                "tz:DtcToezichter.voornaam": "Jan",
                "tz:DtcToezichter.naam": "Bosmans",
                "tz:DtcToezichter.gebruikersnaam": "bosmanja"
            },
            "loc:Locatie.omschrijving": "",
            "tz:Schadebeheerder.schadebeheerder": {
                "tz:DtcBeheerder.naam": "District Brecht",
                "tz:DtcBeheerder.referentie": "123"
            },
            "AIMToestand.toestand": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlAIMToestand/in-gebruik",
            "loc:Locatie.geometrie": ""
        }],
        'otl/betrokkenerelaties/search/000a35d5-c4a5-4a36-8620-62c99e053ba0': [
            {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#HeeftBetrokkene",
                "@id": "https://data.awvvlaanderen.be/id/assetrelatie/1cdb583d-c1b9-4d74-8bb3-9556a5e59a2b-b25kZXJkZWVsI0hlZWZ0QmV0cm9ra2VuZQ",
                "RelatieObject.bron": {
                    "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                    "@id": "https://data.awvvlaanderen.be/id/asset/000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "RelatieObject.doel": {
                    "@type": "http://purl.org/dc/terms/Agent",
                    "@id": "https://data.awvvlaanderen.be/id/asset/35de1da1-8ef3-45bf-bf91-cdb23e0889cc-cHVybDpBZ2VudA"
                },
                "HeeftBetrokkene.rol": "https://wegenenverkeer.data.vlaanderen.be/id/concept/KlBetrokkenheidRol/toezichtsgroep",
                "HeeftBetrokkene.specifiekeContactinfo": [],
                "AIMDBStatus.isActief": True
            }
        ],
        'otl/assetrelaties/search/000a35d5-c4a5-4a36-8620-62c99e053ba0': [
            {
                "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging",
                "@id": "https://data.awvvlaanderen.be/id/assetrelatie/cb9aa0d4-b6ad-474f-9aef-345408313a64-b25kZXJkZWVsI0JldmVzdGlnaW5n",
                "RelatieObject.bron": {
                    "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkpoort",
                    "@id": "https://data.awvvlaanderen.be/id/asset/000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "RelatieObject.doel": {
                    "@type": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Netwerkelement",
                    "@id": "https://data.awvvlaanderen.be/id/asset/bbac4a9a-905a-4991-bafa-43126fb5db10-b25kZXJkZWVsI05ldHdlcmtlbGVtZW50"
                },
                "RelatieObject.typeURI": "https://wegenenverkeer.data.vlaanderen.be/ns/onderdeel#Bevestiging",
                "AIMDBStatus.isActief": True,
                "RelatieObject.bronAssetId": {
                    "DtcIdentificator.toegekendDoor": "AWV",
                    "DtcIdentificator.identificator": "000a35d5-c4a5-4a36-8620-62c99e053ba0-b25kZXJkZWVsI05ldHdlcmtwb29ydA"
                },
                "RelatieObject.doelAssetId": {
                    "DtcIdentificator.toegekendDoor": "AWV",
                    "DtcIdentificator.identificator": "bbac4a9a-905a-4991-bafa-43126fb5db10-b25kZXJkZWVsI05ldHdlcmtlbGVtZW50"
                },
                "RelatieObject.assetId": {
                    "DtcIdentificator.identificator": "cb9aa0d4-b6ad-474f-9aef-345408313a64-b25kZXJkZWVsI0JldmVzdGlnaW5n",
                    "DtcIdentificator.toegekendDoor": "AWV"
                }
            }
        ],
        'otl/agents/search/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0': [{
            "@type": "http://purl.org/dc/terms/Agent",
            "@id": "https://data.awvvlaanderen.be/id/asset/a9d7c44c-0daf-4d3a-bffc-074afb5f54c0-cHVybDpBZ2VudA",
            "purl:Agent.naam": "nieuwe_naam",
            "purl:Agent.contactinfo": []
        }],
    }
