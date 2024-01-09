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
def author_doc():
    text = """
    <div class="bio">
     <div class="bio_title">
      Siobhan Clarke
     </div>
     <table class="bio_table">
      <tbody>
       <tr class="evengrey top">
        <td>
         Affiliation:
        </td>
        <td>
         Trinity College Dublin
        </td>
       </tr>
       <tr class="oddgrey bottom">
        <td>
         Web page:
        </td>
        <td>
         <a href="https://www.cs.tcd.ie/Siobhan.Clarke/" target="_blank">
          https://www.cs.tcd.ie/Siobhan.Clarke/
         </a>
        </td>
       </tr>
      </tbody>
     </table>
    </div>
    """
    return as_document(text)


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
