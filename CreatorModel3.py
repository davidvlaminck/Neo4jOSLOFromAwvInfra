import json

from AbstractCreator import AbstractCreator


class CreatorModel2(AbstractCreator):
    def create_relatie_from_jsonLd_dict(self, json_dict):
        raise NotImplementedError

    def create_asset_from_jsonLd_dict(self, json_dict):
        raise NotImplementedError

# Model3 zal de attributen en de attribuutwaarden als nodes modelleren voor de niet gemeenschappelijke attributen (attributen niet van AIMObject, AIMNaamObject of NaampadObject)
# De node van de attribuutwaarde zal als label de verkorte uri van het type hebben en een property value met de ingevulde waarde
# De node van het attribuut heeft als label de verkorte uri
# er worden 3 relaties gelegd:
# tussen de asset en het attribuut: zo weet je welke attributen het asset heeft
# tussen het attribuut en de attribuutwaarde: zo weet je welke mogelijke waarde dat attribuut heeft
# tussen de asset en attribuutwaarde: zo weet je welke ingevulde waarde die asset voor dat attribuut heeft
