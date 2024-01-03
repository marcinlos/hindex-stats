from dataclasses import dataclass
from typing import List


@dataclass
class Author:
    name: str
    affiliation: str
    interests: List[str]
    hindex: int
    profile: str
