from pathlib import Path

import pytest
from bs4 import BeautifulSoup

import hindex_stats.scrap.iccs_smart_program as scrap
import tests.data as data


def load_document(name):
    with data.load(Path("scrap/iccs") / name) as source:
        return BeautifulSoup(source, "html.parser")


def load_tag(name):
    doc = load_document(name)
    return doc.find()


def as_tag(text):
    doc = BeautifulSoup(text, "html.parser")
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


@pytest.fixture()
def talk_tag():
    text = """
    <tr class="talk">
    <td class="time">
    10:40
    </td>
    <td>
    <a name="talk:168617">
    </a>
    <div class="authors">
        <a name="talk:168617">
        </a>
        <a class="person"
        href="https://easychair.org/smart-program/ICCS2021/person1649.html">
        Jose Monreal Bailey
        </a>
        ,
        <a class="person"
        href="https://easychair.org/smart-program/ICCS2021/person1650.html">
        Hadi Tabatabaee Malazi
        </a>
        and
        <a class="person"
        href="https://easychair.org/smart-program/ICCS2021/person1651.html">
        Siobhan Clarke
        </a>
    </div>
    <div class="title">
        Smoothing Speed Variability in Age-Friendly Urban Traffic Management
        <span style="font-weight:normal;white-space:nowrap">
        (
        <a href="https://easychair.org/smart-program/ICCS2021/2021-06-16.html#talk:168617">
        abstract
        </a>
        )
        </span>
    </div>
    </td>
    </tr>
    """
    return as_tag(text)


@pytest.fixture()
def session_tag():
    return load_tag("session.html")


@pytest.fixture()
def coffee_break_tag():
    text = """
    <div class="session">
     <div class="coffeebreak">
      <span class="interval">
       10:10-10:40
      </span>
      <span class="title">
       Coffee Break
      </span>
     </div>
    </div>
    """
    return as_tag(text)


@pytest.fixture()
def author_doc():
    return load_document("author.html")


def test_parsing_author_occurence(author_occurence_tag):
    result = scrap._parse_author_occurrence(author_occurence_tag)

    expected = scrap.AuthorOccurrence(
        "Marco Viceconti",
        "https://easychair.org/smart-program/ICCS2021/person2096.html",
    )

    assert result == expected


def test_parsing_talk(talk_tag):
    result = scrap._parse_talk(talk_tag)

    expected = scrap.Talk(
        title="Smoothing Speed Variability in Age-Friendly Urban Traffic Management",
        authors=[
            scrap.AuthorOccurrence(
                "Jose Monreal Bailey",
                "https://easychair.org/smart-program/ICCS2021/person1649.html",
            ),
            scrap.AuthorOccurrence(
                "Hadi Tabatabaee Malazi",
                "https://easychair.org/smart-program/ICCS2021/person1650.html",
            ),
            scrap.AuthorOccurrence(
                "Siobhan Clarke",
                "https://easychair.org/smart-program/ICCS2021/person1651.html",
            ),
        ],
    )

    assert result == expected


def test_parsing_author_page(author_doc):
    result = scrap._parse_author_page(author_doc)
    expected = scrap.AuthorDetails("Trinity College Dublin")
    assert result == expected


@pytest.mark.parametrize(
    ("label", "expected"),
    [
        ("Session 6A: MT 5", ("MT", 5)),
        ("Session 4J: SE4Science 1", ("SE4Science", 1)),
        ("Session 5: Keynote Lecture 2", ("Keynote Lecture", 2)),
        ("Session 6C: AIHPC4AS 3", ("AIHPC4AS", 3)),
        ("Coffee Break", None),
    ],
)
def test_parsing_session_label(label, expected):
    result = scrap._parse_session_label(label)
    assert result == expected


def test_parsing_session(session_tag):
    result = scrap._parse_session(session_tag)
    expected = scrap.Session(
        name="MT",
        number=1,
        talks=[
            scrap.Talk(
                title="Smoothing Speed Variability in Age-Friendly "
                "Urban Traffic Management",
                authors=[
                    scrap.AuthorOccurrence(
                        "Jose Monreal Bailey",
                        "https://easychair.org/smart-program/ICCS2021/person1649.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Hadi Tabatabaee Malazi",
                        "https://easychair.org/smart-program/ICCS2021/person1650.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Siobhan Clarke",
                        "https://easychair.org/smart-program/ICCS2021/person1651.html",
                    ),
                ],
            ),
            scrap.Talk(
                title="An innovative employment of NetLogo AIDS model in developing "
                "a new chain coding mechanism for compression",
                authors=[
                    scrap.AuthorOccurrence(
                        "Khaldoon Dhou",
                        "https://easychair.org/smart-program/ICCS2021/person1439.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Christopher Cruzen",
                        "https://easychair.org/smart-program/ICCS2021/person1440.html",
                    ),
                ],
            ),
            scrap.Talk(
                title="Simulation modeling of epidemic risk in supermarkets: "
                "Investigating the impact of social distancing and "
                "checkout zone design",
                authors=[
                    scrap.AuthorOccurrence(
                        "Tomasz Antczak",
                        "https://easychair.org/smart-program/ICCS2021/person1301.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Bartosz Skorupa",
                        "https://easychair.org/smart-program/ICCS2021/person1302.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Mikolaj Szurlej",
                        "https://easychair.org/smart-program/ICCS2021/person1303.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Rafal Weron",
                        "https://easychair.org/smart-program/ICCS2021/person1304.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Jacek Zabawa",
                        "https://easychair.org/smart-program/ICCS2021/person1305.html",
                    ),
                ],
            ),
            scrap.Talk(
                title="A multi-cell cellular automata model of traffic flow "
                "with emergency vehicles: effect of a corridor of life",
                authors=[
                    scrap.AuthorOccurrence(
                        "Krzysztof Małecki",
                        "https://easychair.org/smart-program/ICCS2021/person905.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Marek Kamiński",
                        "https://easychair.org/smart-program/ICCS2021/person906.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Jarosław Wąs",
                        "https://easychair.org/smart-program/ICCS2021/person907.html",
                    ),
                ],
            ),
            scrap.Talk(
                title="HSLF: HTTP Header Sequence based LSH fingerprints "
                "for Application Traffic Classification",
                authors=[
                    scrap.AuthorOccurrence(
                        "Zixian Tang",
                        "https://easychair.org/smart-program/ICCS2021/person910.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Qiang Wang",
                        "https://easychair.org/smart-program/ICCS2021/person911.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Wenhao Li",
                        "https://easychair.org/smart-program/ICCS2021/person807.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Huaifeng Bao",
                        "https://easychair.org/smart-program/ICCS2021/person808.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Wen Wang",
                        "https://easychair.org/smart-program/ICCS2021/person912.html",
                    ),
                    scrap.AuthorOccurrence(
                        "Feng Liu",
                        "https://easychair.org/smart-program/ICCS2021/person810.html",
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parsing_session_coffee_break(coffee_break_tag):
    result = scrap._parse_session(coffee_break_tag)
    assert result is None
