from dataclasses import dataclass
from enum import Flag, auto


@dataclass
class Query:
    name: str
    affiliation: str | None


class InfoType(Flag):
    NONE = 0
    HINDEX = auto()


@dataclass
class AuthorEntry:
    name: str
    affiliation: str
    scholar_id: str
    email: str | None
    interests: list[str]
    hindex: int | None
    citations: int | None
