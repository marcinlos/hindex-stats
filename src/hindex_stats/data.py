from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AuthorEntry:
    name: str
    affiliation: str
    scholar_id: str
    email: Optional[str]
    interests: List[str]
    hindex: Optional[int]
    citations: Optional[int]
