from CreatorModel1 import CreatorModel1
from EMInfraImporter import EMInfraImporter
from Neo4JConnector import Neo4JConnector

test_dataset = ["0043f983-8eec-414d-8a78-ab6bef8f0dad", "00913b07-74b2-43e7-9123-806f8b70a184",
                "01011cca-78f5-44de-a242-f9fea60cfe89", "010d3efc-5e15-40d4-998e-1f641dc3a1ac",
                "01c642bd-d09b-4818-b622-aa929c682331", "01f4fb1f-e798-4880-8054-d7950d8b592c",
                "01f525d3-ceae-4251-bae2-f1b7b9110e29", "022ffa30-2db0-41c7-95bd-06f0ce03277a",
                "0235e666-0437-4700-82fc-cccfe80003f4", "02504df6-44cf-4b7c-8343-69951fb06c87",
                "2d1249e6-318c-4312-a1f9-15a481c2afb1", "bcf9fcf2-f36a-4ac0-b07a-ca57b718bd01",
                "1ea75c80-769f-4c00-80c1-d09abaa52d28", "517ad8a1-daa2-490a-a1a7-36781bb0bc30",
                "e6185608-14ea-47a4-aac9-5cbee8687a8c", "942d7046-52cd-4f65-bf05-f79738a006ea",
                "73c56de7-02b0-4c17-922d-d2c018366e6e", "bfe0e434-ffc7-466f-9d23-e173639545a4",
                "11604e6a-a515-452b-bdcc-f4c7fe9b96bc", "b94867e2-26b3-40e8-915c-e12e1c59eafc",
                "1711cd89-e20a-414a-8b7a-13dd252100e8", "3ef57e1c-8d28-4870-b33c-ab295c436523",
                "93067e4d-1851-4ae2-b250-eaca2ed8925e", "23a2839a-39d4-4244-9e9a-ad6f92cce90f",
                "82ee20d5-9f4c-47a3-ac18-1fd8661585be", "31029ab8-248e-47f9-8df6-a7030342b01a",
                "b94aacc7-e85a-47ee-987e-0ac468815b01", "8c893703-2248-485b-a7b3-3d08fcf7b7ff",
                "5296e967-e59a-4541-9fe7-d8361dc14f7f", "c6f107f2-0778-486b-9354-afd97faebd36",
                "76a77c4f-f704-4f35-ab7c-fb709029a011", "e8443eac-4955-4a44-9793-0f88751130d1",
                "f501ee09-9911-4665-b85e-0c4d6553da73", "0a03c59d-10fe-47b1-9282-74d4a3205593",
                "7d7f6e7f-a168-4b59-ae05-199ad81c3c7c", "e44ec4d6-90f5-41a5-97c0-7f965ff391d4",
                "ae23a066-d6fc-466b-b6ea-ded99721743b", "f195cad2-a985-463e-aad0-1eea8013a4b9",
                "db6ddd51-9722-47e1-86e9-37fd235f4554", "c481ba25-aca0-49d8-a0b4-56bd33e4555a",
                "0b5546f5-0785-4866-9a3f-7ffcd380e06b", "80551a4e-1310-4e13-a218-f46868df4df6",
                "3964053e-94ad-47fd-9820-46696f49674e", "78ed6862-93b3-47ae-be38-2fe70da31fa9",
                "e21f5f36-dbfe-46cb-b69e-6e0d8e3e96a8", "5ec5ae02-6c3b-436e-a5d6-250fad0287a4",
                "238f52fc-0e20-4dbe-8ef6-0914e5768610", "486706c5-b5ff-4260-b21f-c0f5c47e22dd",
                "454240f6-c4a1-48b3-8a1f-5eabcc208718", "59e0b6d3-35fb-48ab-9651-1be20bda1418",
                "6dcf04ef-7f09-42ec-9acd-797efdec1c16", "b689d1b8-0073-4e92-bea3-ffdb754c1fe2",
                "2564929f-5824-48c8-993f-84a3fe1da975", "8873f140-e8d4-470a-8519-b9c200e15da9",
                "f0946e2b-d01e-481f-8506-21f95d7107e4", "0cd0e47f-f2a4-4951-bd02-dba9de23568b",
                "89f33132-664e-470c-ad7d-f42f1cdea02a", "8dfff712-4211-4d95-aa4b-932b2d5f740c",
                "30961931-75cf-46b0-a2f1-04ed9ac32eeb", "f229567c-d1e3-4a61-b732-a7241fac6a25",
                "ad3bb42d-de35-47d3-ae62-cfb75156d43d", "8a4bec31-b360-45ec-a605-247737881ee9",
                "d215a115-3941-4509-b45d-4921fc626cbe", "fbeba1a9-fd01-4f87-9de3-850994e6990c",
                "88297d65-cd06-4356-83f3-d46658f65091", "5a87621b-1c45-4b89-8e47-783e709dcdd2",
                "9b6eec7c-0d02-4447-8a74-26f17bc7be96", "290ff489-44fa-48b8-8ab4-f43ee8501643",
                "02f52470-27c0-44e3-a29f-751a0bd6a0ed"]

if __name__ == "__main__":
    importer = EMInfraImporter(cert_path='C:\\resources\\datamanager_eminfra_prd.awv.vlaanderen.be.crt',
                               key_path='C:\\resources\\datamanager_eminfra_prd.awv.vlaanderen.be.key')
    connector = Neo4JConnector("bolt://localhost:7687", "neo4jPython", "python")
    creator = CreatorModel1(neo4JConnector=connector, eminfraImporter=importer)

    creator.create_assets_from_eminfra(test_dataset)
    creator.create_relaties_from_eminfra(test_dataset)

    connector.close()
