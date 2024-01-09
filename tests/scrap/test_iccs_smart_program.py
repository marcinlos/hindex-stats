import pytest
from bs4 import BeautifulSoup

import hindex_stats.scrap.iccs_smart_program as scrap


def as_document(text):
    return BeautifulSoup(text, "html.parser")


def as_tag(text):
    doc = as_document(text)
    return doc.find()


@pytest.fixture()
def author_occurence_tag():
    text = """
    <a class="person"
    href="https://easychair.org/smart-program/ICCS2021/person2096.html">
    Marco Viceconti
    </a>
    """
    return as_tag(text)


def test_parsing_author_occurence(author_occurence_tag):
    result = scrap._parse_author_occurrence(author_occurence_tag)

    expected = scrap.AuthorOccurrence(
        "Marco Viceconti",
        "https://easychair.org/smart-program/ICCS2021/person2096.html",
    )

    assert result == expected
