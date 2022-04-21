import logging

from neo4j import Transaction

from EMInfraImporter import EMInfraImporter
from EventProcessors.RelatieProcessor import RelatieProcessor
from EventProcessors.RelationNotCreatedError import RelationNotCreatedError, AssetRelationNotCreatedError
from EventProcessors.SpecificEventProcessor import SpecificEventProcessor


class AssetRelatiesGewijzigdProcessor(SpecificEventProcessor, RelatieProcessor):
    def __init__(self, tx_context: Transaction, emInfraImporter: EMInfraImporter):
        super().__init__(tx_context, emInfraImporter)

    def process(self, uuids: [str]):
        assetrelatie_dicts = self.emInfraImporter.import_assetrelaties_from_webservice_by_assetuuids(asset_uuids=uuids)

        self.process_dicts(assetrelatie_dicts, uuids)

    def process_dicts(self, assetrelatie_dicts, uuids: {str}):
        logging.info(f'started creating {len(assetrelatie_dicts)} assetrelaties')
        self.remove_all_asset_relaties(list(uuids))
        relaties_created = self.create_assetrelaties_from_list_of_jsondicts(assetrelatie_dicts)
        if relaties_created < len(assetrelatie_dicts):
            raise RuntimeError
        logging.info('done')

    def create_assetrelaties_from_list_of_jsondicts(self, assetrelatie_dicts):
        paramslist = self.create_paramslist_from_list_of_jsondicts(assetrelatie_dicts)
        query = "UNWIND $params as row " \
                "MATCH (a:Asset {uuid: row.bron_uuid}) " \
                "MATCH (b:Asset {uuid: row.doel_uuid}) " \
                "CALL apoc.create.relationship(a, row.relatie_type, row.relatie_dict, b) " \
                "YIELD rel " \
                "RETURN count(rel);"
        return self.tx_context.run(query, params=paramslist).single()[0]

    def create_paramslist_from_list_of_jsondicts(self, assetrelatie_dicts):
        param_list = []
        for json_dict in assetrelatie_dicts:
            relatie_dict = {'assetIdUri': json_dict['@id'], 'typeURI': json_dict['@type'],
                            'isActief': json_dict["AIMDBStatus.isActief"],
                            'uuid': json_dict['RelatieObject.assetId']['DtcIdentificator.identificator'][0:36]}

            bron_uuid = json_dict['RelatieObject.bronAssetId']['DtcIdentificator.identificator'][0:36]
            doel_uuid = json_dict['RelatieObject.doelAssetId']['DtcIdentificator.identificator'][0:36]
            relatie_type = json_dict["RelatieObject.typeURI"].split('#')[1]

            for k, v in json_dict.items():
                if k in ['@type', '@id', "RelatieObject.doel", "RelatieObject.assetId", "AIMDBStatus.isActief",
                         "RelatieObject.bronAssetId", "RelatieObject.doelAssetId", "RelatieObject.typeURI", "RelatieObject.bron"]:
                    continue
                if isinstance(v, dict):
                    relatie_dict[k] = json.dumps(v)
                else:
                    relatie_dict[k] = v

            param_list.append({'bron_uuid': bron_uuid,
                               'doel_uuid': doel_uuid,
                               'relatie_type': relatie_type,
                               'relatie_dict': relatie_dict})

        return param_list