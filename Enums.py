from enum import Enum


class Environment(Enum):
    PRD = 'prd',
    DEV = 'dev',
    TEI = 'tei',
    AIM = 'aim'
    edison_acc = 'edison-acc'
    edison = 'edison'


class AuthType(Enum):
    JWT = 'JWT',
    CERT = 'cert',
    COOKIE = 'cookie'
    local = 'local'
