from dataclasses import dataclass

from bs4 import Tag


@dataclass
class AuthorOccurrence:
    name: str
    link: str


def _parse_author_occurrence(tag: Tag) -> AuthorOccurrence:
    name = tag.text.strip()
    link = tag["href"]
    return AuthorOccurrence(name, link)
