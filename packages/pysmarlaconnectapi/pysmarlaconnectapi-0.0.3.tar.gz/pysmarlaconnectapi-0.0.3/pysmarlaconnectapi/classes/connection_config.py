from dataclasses import dataclass

from . import AuthToken


@dataclass
class ConnectionConfig:
    url: str
    token: AuthToken
