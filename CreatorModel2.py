import json

from AbstractCreator import AbstractCreator


class CreatorModel2(AbstractCreator):
    def create_relatie_from_jsonLd_dict(self, json_dict):
        raise NotImplementedError

    def create_asset_from_jsonLd_dict(self, json_dict):
        raise NotImplementedError

# Model2 zal de attribuutwaarden als nodes modelleren voor de niet gemeenschappelijke attributen (attributen niet van AIMObject, AIMNaamObject of NaampadObject)
# De node zal als label de verkorte uri van het type hebben en een property value met de ingevulde waarde
# de relatie tussen de asset en de node zal als type de verkorte uri hebben
