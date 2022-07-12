from dataclasses import dataclass
from typing import Dict, Any


class BaseDataClass:
    def dict(self):
        return self.__dict__


@dataclass
class DuckieBot(BaseDataClass):
    hostname: str


@dataclass
class User(BaseDataClass):
    name: str = "Unknown"
    role: str = "Unknown"
    user_jwt: str = ""


@dataclass
class DuckieBotSession(BaseDataClass):
    id: int
    owner: str
    hostname: str
    start_time: Dict[str, Any]
    end_time: Dict[str, Any]


@dataclass
class TGUser(BaseDataClass):
    tg_chat_id: int
    tg_github_name: str = "Unknown"
