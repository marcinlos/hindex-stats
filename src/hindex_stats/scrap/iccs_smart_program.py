from dataclasses import dataclass

from bs4 import Tag


@dataclass
class AuthorOccurrence:
    name: str
    link: str


@dataclass
class Talk:
    title: str
    authors: list[AuthorOccurrence]


def _parse_author_occurrence(tag: Tag) -> AuthorOccurrence:
    name = tag.text.strip()
    link = tag["href"]
    return AuthorOccurrence(name, link)


def _parse_talk(tag: Tag) -> Talk:
    title_tag = tag.find("div", {"class": "title"})
    title = next(title_tag.stripped_strings)

    author_tags = tag.find_all("a", {"class": "person"})
    authors = [_parse_author_occurrence(tag) for tag in author_tags]

    return Talk(title, authors)
