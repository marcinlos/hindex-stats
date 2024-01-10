from pathlib import Path

import pytest
from bs4 import BeautifulSoup

import hindex_stats.scrap.iccs.parser as parser
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


@pytest.fixture()
def program_doc():
    return load_document("program.html")


def test_parsing_author_occurence(author_occurence_tag):
    result = parser._parse_author_occurrence(author_occurence_tag)

    expected = parser.AuthorOccurrence(
        "Marco Viceconti",
        "https://easychair.org/smart-program/ICCS2021/person2096.html",
    )

    assert result == expected


def test_parsing_talk(talk_tag):
    result = parser._parse_talk(talk_tag)

    expected = parser.Talk(
        title="Smoothing Speed Variability in Age-Friendly Urban Traffic Management",
        authors=[
            parser.AuthorOccurrence(
                "Jose Monreal Bailey",
                "https://easychair.org/smart-program/ICCS2021/person1649.html",
            ),
            parser.AuthorOccurrence(
                "Hadi Tabatabaee Malazi",
                "https://easychair.org/smart-program/ICCS2021/person1650.html",
            ),
            parser.AuthorOccurrence(
                "Siobhan Clarke",
                "https://easychair.org/smart-program/ICCS2021/person1651.html",
            ),
        ],
    )

    assert result == expected


def test_parsing_author_page(author_doc):
    result = parser.parse_author_page(author_doc)
    expected = parser.AuthorDetails("Trinity College Dublin")
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
    result = parser._parse_session_label(label)
    assert result == expected


def test_parsing_session(session_tag):
    result = parser._parse_session(session_tag)
    expected = parser.Session(
        name="MT",
        number=1,
        talks=[
            parser.Talk(
                title="Smoothing Speed Variability in Age-Friendly "
                "Urban Traffic Management",
                authors=[
                    parser.AuthorOccurrence(
                        "Jose Monreal Bailey",
                        "https://easychair.org/smart-program/ICCS2021/person1649.html",
                    ),
                    parser.AuthorOccurrence(
                        "Hadi Tabatabaee Malazi",
                        "https://easychair.org/smart-program/ICCS2021/person1650.html",
                    ),
                    parser.AuthorOccurrence(
                        "Siobhan Clarke",
                        "https://easychair.org/smart-program/ICCS2021/person1651.html",
                    ),
                ],
            ),
            parser.Talk(
                title="An innovative employment of NetLogo AIDS model in developing "
                "a new chain coding mechanism for compression",
                authors=[
                    parser.AuthorOccurrence(
                        "Khaldoon Dhou",
                        "https://easychair.org/smart-program/ICCS2021/person1439.html",
                    ),
                    parser.AuthorOccurrence(
                        "Christopher Cruzen",
                        "https://easychair.org/smart-program/ICCS2021/person1440.html",
                    ),
                ],
            ),
            parser.Talk(
                title="Simulation modeling of epidemic risk in supermarkets: "
                "Investigating the impact of social distancing and "
                "checkout zone design",
                authors=[
                    parser.AuthorOccurrence(
                        "Tomasz Antczak",
                        "https://easychair.org/smart-program/ICCS2021/person1301.html",
                    ),
                    parser.AuthorOccurrence(
                        "Bartosz Skorupa",
                        "https://easychair.org/smart-program/ICCS2021/person1302.html",
                    ),
                    parser.AuthorOccurrence(
                        "Mikolaj Szurlej",
                        "https://easychair.org/smart-program/ICCS2021/person1303.html",
                    ),
                    parser.AuthorOccurrence(
                        "Rafal Weron",
                        "https://easychair.org/smart-program/ICCS2021/person1304.html",
                    ),
                    parser.AuthorOccurrence(
                        "Jacek Zabawa",
                        "https://easychair.org/smart-program/ICCS2021/person1305.html",
                    ),
                ],
            ),
            parser.Talk(
                title="A multi-cell cellular automata model of traffic flow "
                "with emergency vehicles: effect of a corridor of life",
                authors=[
                    parser.AuthorOccurrence(
                        "Krzysztof Małecki",
                        "https://easychair.org/smart-program/ICCS2021/person905.html",
                    ),
                    parser.AuthorOccurrence(
                        "Marek Kamiński",
                        "https://easychair.org/smart-program/ICCS2021/person906.html",
                    ),
                    parser.AuthorOccurrence(
                        "Jarosław Wąs",
                        "https://easychair.org/smart-program/ICCS2021/person907.html",
                    ),
                ],
            ),
            parser.Talk(
                title="HSLF: HTTP Header Sequence based LSH fingerprints "
                "for Application Traffic Classification",
                authors=[
                    parser.AuthorOccurrence(
                        "Zixian Tang",
                        "https://easychair.org/smart-program/ICCS2021/person910.html",
                    ),
                    parser.AuthorOccurrence(
                        "Qiang Wang",
                        "https://easychair.org/smart-program/ICCS2021/person911.html",
                    ),
                    parser.AuthorOccurrence(
                        "Wenhao Li",
                        "https://easychair.org/smart-program/ICCS2021/person807.html",
                    ),
                    parser.AuthorOccurrence(
                        "Huaifeng Bao",
                        "https://easychair.org/smart-program/ICCS2021/person808.html",
                    ),
                    parser.AuthorOccurrence(
                        "Wen Wang",
                        "https://easychair.org/smart-program/ICCS2021/person912.html",
                    ),
                    parser.AuthorOccurrence(
                        "Feng Liu",
                        "https://easychair.org/smart-program/ICCS2021/person810.html",
                    ),
                ],
            ),
        ],
    )
    assert result == expected


def test_parsing_session_coffee_break(coffee_break_tag):
    result = parser._parse_session(coffee_break_tag)
    assert result is None


def test_parsing_program_page(program_doc):
    result = parser.parse_program_page(program_doc)

    assert len(result) == 85

    tracks = set(session.name for session in result)
    expected = set(
        [
            "Keynote Lecture",
            "MT",
            "AIHPC4AS",
            "BBC",
            "COMS",
            "SOFTMAC",
            "CLDD",
            "CSOC",
            "DisA",
            "CMSA",
            "IoTSS",
            "ACMAIML",
            "SE4Science",
            "MESHFREE",
            "CompHealth",
            "QCW",
            "MMS",
            "MLDADS",
            "SmartSys",
            "CGIPAI",
            "SPU",
            "CCI",
            "DDCS",
            "WTCS",
            "UNEQUIvOCAL",
        ]
    )

    assert tracks == expected
