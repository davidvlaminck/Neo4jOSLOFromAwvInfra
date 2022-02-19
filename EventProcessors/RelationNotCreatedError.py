class RelationNotCreatedError(Exception):
    pass


class AssetRelationNotCreatedError(RelationNotCreatedError):
    pass


class BetrokkeneRelationNotCreatedError(RelationNotCreatedError):
    pass