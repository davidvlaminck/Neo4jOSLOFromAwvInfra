class RelationNotCreatedError(Exception):
    pass


class AssetRelationNotCreatedError(RelationNotCreatedError):
    def __init__(self, message, asset_uuids: list = None):
        super().__init__(message)
        self.asset_uuids = asset_uuids


class BetrokkeneRelationNotCreatedError(RelationNotCreatedError):
    def __init__(self, message, asset_uuids: list = None, agent_uuids: list = None):
        super().__init__(message)
        if asset_uuids is None:
            asset_uuids = []
        if agent_uuids is None:
            agent_uuids = []
        self.asset_uuids = asset_uuids
        self.agent_uuids = agent_uuids
