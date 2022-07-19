class RelationNotCreatedError(Exception):
    pass


class AssetRelationNotCreatedError(RelationNotCreatedError):
    def __init__(self, message, asset_uuids: list = None):
        super().__init__(message)
        self.asset_uuids = asset_uuids


class BetrokkeneRelationNotCreatedError(RelationNotCreatedError):
    pass
