import re
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag


@dataclass
class AuthorOccurrence:
    name: str
    link: str


@dataclass
class Talk:
    title: str
    authors: list[AuthorOccurrence]


@dataclass
class AuthorDetails:
    affiliation: str


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


def _parse_author_page(doc: BeautifulSoup) -> AuthorDetails:
    label_tag = doc.find("td", string=re.compile("Affiliation"))
    affiliation_tag = label_tag.find_next("td")

    affiliation = affiliation_tag.text.strip()

    return AuthorDetails(affiliation)


def _parse_session_label(label: str) -> tuple[str, int] | None:
    match = re.match(r"Session \w+: (.+) (\d+)", label)
    if match:
        name = match.group(1)
        number = int(match.group(2))
        return (name, number)
    else:
        return None
