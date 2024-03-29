import re
from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

from hindex_stats.utils import without_none


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


@dataclass
class Session:
    name: str
    number: int
    talks: list[Talk]


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


def parse_author_page(doc: BeautifulSoup) -> AuthorDetails:
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


def _parse_session(tag: Tag) -> Session | None:
    label_tag = tag.find("span", {"class": "title"})
    label = label_tag.text.strip()
    match _parse_session_label(label):
        case (name, number):
            talk_tags = tag.find_all("tr", {"class": "talk"})
            talks = [_parse_talk(t) for t in talk_tags]
            return Session(name, number, talks)


def parse_program_page(doc: BeautifulSoup) -> list[Session]:
    session_tags = doc.find_all("div", {"class": "session"})
    return list(without_none(map(_parse_session, session_tags)))
