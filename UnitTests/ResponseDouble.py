class ResponseDouble:
    page_locatie_gewijzigd = {'id': 'Proxied EM-Infra change feed for assets', 'base': '/feed/assets',
                              'title': 'Proxied EM-Infra change feed for assets',
                              'generator': {'text': 'Default Feed provider', 'uri': 'https://github.com/WegenenVerkeer/atomium',
                                            'version': '1.0'}, 'updated': '2021-02-16T22:33:02+01:00',
                              'links': [{'rel': 'self', 'href': '/250/1'}, {'rel': 'last', 'href': '/0/1'},
                                        {'rel': 'next', 'href': '/249/1'}, {'rel': 'previous', 'href': '/251/1'}], 'entries': [
            {'_type': 'atom', 'updated': '2021-02-16T22:33:02+01:00', 'id': 'c11d1fb8-b37d-43c4-9e7a-7c3a34f28c55', 'content': {
                'value': {'event-type': 'LOCATIE_GEWIJZIGD', 'asset-type': 'installatie', 'event-id': '4581934',
                          'uuids': ['5646715c-b067-4a1f-9bf4-0f27d439c7f9']}}}]}
    page_nieuwe_installatie = {'id': 'Proxied EM-Infra change feed for assets', 'base': '/feed/assets',
                               'title': 'Proxied EM-Infra change feed for assets',
                               'generator': {'text': 'Default Feed provider', 'uri': 'https://github.com/WegenenVerkeer/atomium',
                                             'version': '1.0'}, 'updated': '2021-02-16T20:19:10+01:00',
                               'links': [{'rel': 'self', 'href': '/0/1'}, {'rel': 'last', 'href': '/0/1'},
                                         {'rel': 'previous', 'href': '/1/1'}], 'entries': [
            {'_type': 'atom', 'updated': '2021-02-16T20:19:10+01:00', 'id': '11899cdb-5668-4dd3-9010-4ebed23f80a1', 'content': {
                'value': {'event-type': 'NIEUWE_INSTALLATIE', 'asset-type': 'installatie',
                          'uuids': ['5646715c-b067-4a1f-9bf4-0f27d439c7f9', '00502271-e64b-41d9-8bdb-0897f099561c',
                                    '00f27c6a-cd1a-4e13-b68b-cf44ac8d9c13']}}}]}
    page_naampad_gewijzigd = {'id': 'Proxied EM-Infra change feed for assets', 'base': '/feed/assets',
                              'title': 'Proxied EM-Infra change feed for assets',
                              'generator': {'text': 'Default Feed provider', 'uri': 'https://github.com/WegenenVerkeer/atomium',
                                            'version': '1.0'}, 'updated': '2021-02-17T11:22:03+01:00',
                              'links': [{'rel': 'self', 'href': '/1000/1'}, {'rel': 'last', 'href': '/0/1'},
                                        {'rel': 'next', 'href': '/999/1'}, {'rel': 'previous', 'href': '/1001/1'}], 'entries': [
            {'_type': 'atom', 'updated': '2021-02-17T11:22:03+01:00', 'id': 'fa0aa99a-cf87-44d2-86c3-f087317f985a', 'content': {
                'value': {'event-type': 'NAAMPAD_GEWIJZIGD', 'asset-type': 'installatie', 'event-id': '4582640',
                          'uuids': ['5646715c-b067-4a1f-9bf4-0f27d439c7f9']}}}]}
    page_eigenschappen_gewijzigd = {'id': 'Proxied EM-Infra change feed for assets', 'base': '/feed/assets',
                                    'title': 'Proxied EM-Infra change feed for assets',
                                    'generator': {'text': 'Default Feed provider',
                                                  'uri': 'https://github.com/WegenenVerkeer/atomium', 'version': '1.0'},
                                    'updated': '2021-02-17T11:22:09+01:00',
                                    'links': [{'rel': 'self', 'href': '/1500/1'}, {'rel': 'last', 'href': '/0/1'},
                                              {'rel': 'next', 'href': '/1499/1'}, {'rel': 'previous', 'href': '/1501/1'}],
                                    'entries': [{'_type': 'atom', 'updated': '2021-02-17T11:22:09+01:00',
                                                 'id': 'c1be6c00-899e-4b92-880a-0aff9378fbc3', 'content': {
                                            'value': {'event-type': 'EIGENSCHAPPEN_GEWIJZIGD', 'asset-type': 'installatie',
                                                      'event-id': '4583019',
                                                      'uuids': ['5646715c-b067-4a1f-9bf4-0f27d439c7f9']}}}]}
    page_toestand_gewijzigd = {'id': 'Proxied EM-Infra change feed for assets', 'base': '/feed/assets',
                               'title': 'Proxied EM-Infra change feed for assets',
                               'generator': {'text': 'Default Feed provider', 'uri': 'https://github.com/WegenenVerkeer/atomium',
                                             'version': '1.0'}, 'updated': '2021-02-17T11:50:02+01:00',
                               'links': [{'rel': 'self', 'href': '/6000/1'}, {'rel': 'last', 'href': '/0/1'},
                                         {'rel': 'next', 'href': '/5999/1'}, {'rel': 'previous', 'href': '/6001/1'}], 'entries': [
            {'_type': 'atom', 'updated': '2021-02-17T11:50:02+01:00', 'id': '45fd22aa-0a0f-498a-a958-18237fc39511', 'content': {
                'value': {'event-type': 'TOESTAND_GEWIJZIGD', 'asset-type': 'installatie', 'event-id': '4587519',
                          'uuids': ['5646715c-b067-4a1f-9bf4-0f27d439c7f9']}}}]}
    mogelijke_events = ["ACTIEF_GEWIJZIGD", "BESTEK_GEWIJZIGD", "BETROKKENE_RELATIES_GEWIJZIGD", "COMMENTAAR_GEWIJZIGD",
                        "COMMUNICATIEAANSLUITING_GEWIJZIGD", "DOCUMENTEN_GEWIJZIGD", "EIGENSCHAPPEN_GEWIJZIGD",
                        "ELEKTRICITEITSAANSLUITING_GEWIJZIGD", "GEOMETRIE_GEWIJZIGD", "LOCATIE_GEWIJZIGD", "NAAM_GEWIJZIGD",
                        "NAAMPAD_GEWIJZIGD", "NIEUW_ONDERDEEL", "NIEUWE_INSTALLATIE", "PARENT_GEWIJZIGD", "POSTIT_GEWIJZIGD",
                        "RELATIES_GEWIJZIGD", "SCHADEBEHEERDER_GEWIJZIGD", "TOEGANG_GEWIJZIGD", "TOESTAND_GEWIJZIGD",
                        "TOEZICHT_GEWIJZIGD", "VPLAN_GEWIJZIGD", ""]
