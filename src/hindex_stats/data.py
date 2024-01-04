from dataclasses import dataclass
from typing import Optional
from enum import Flag, auto


@dataclass
class Query:
    name: str
    affiliation: Optional[str]


class InfoType(Flag):
    NONE = 0
    HINDEX = auto()


@dataclass
class AuthorEntry:
    name: str
    affiliation: str
    scholar_id: str
    email: Optional[str]
    interests: list[str]
    hindex: Optional[int]
    citations: Optional[int]
