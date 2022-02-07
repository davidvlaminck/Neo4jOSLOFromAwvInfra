from CreatorModel1 import CreatorModel1
from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector

if __name__ == "__main__":
    importer = EMInfraImporter(cert_path='C:\\resources\\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                               key_path='C:\\resources\\datamanager_eminfra_prd.awv.vlaanderen.be.key')
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    creator = CreatorModel1(neo4JConnector=connector, eminfraImporter=importer)

    creator.create_assets_from_eminfra(['6a615585-a9b8-4629-b641-1c6bbdd1ab4c', '000cbd26-eef7-421f-9b81-a88f5210f44a'])
    creator.create_relaties_from_eminfra(['6a615585-a9b8-4629-b641-1c6bbdd1ab4c', '000cbd26-eef7-421f-9b81-a88f5210f44a'])

    connector.close()
