import concurrent.futures
import asyncio
from dataclasses import dataclass
from typing import Callable, Iterable

from scholarly import scholarly

from hindex_stats.utils import take
from hindex_stats.data import AuthorEntry, Query, InfoType


def _author_entry_from_dict(data: dict) -> AuthorEntry:
    return AuthorEntry(
        name=data["name"],
        affiliation=data["affiliation"],
        scholar_id=data["scholar_id"],
        email=data["email_domain"] or None,
        interests=data["interests"],
        hindex=data.get("hindex", None),
        citations=data["citedby"],
    )


def _build_query_string(query: Query) -> str:
    return f"{query.name} {query.affiliation or ''}"


def _section_list(what: InfoType) -> list[str]:
    sections = []
    if InfoType.HINDEX in what:
        sections.append("indices")
    return sections


def search(query: Query, info: InfoType = InfoType.NONE):
    query_string = _build_query_string(query)
    sections = _section_list(info)

    for result in scholarly.search_author(query_string):
        if sections:
            result = scholarly.fill(result, sections=sections)
        yield _author_entry_from_dict(result)


@dataclass
class QueryTask:
    query: Query
    info: InfoType
    max_results: int
    callback: Callable


async def execute_queries(tasks: Iterable[QueryTask], threads: int):
    def go(task):
        for item in take(task.max_results, search(task.query, task.info)):
            task.callback(item)

    # Since scholarly uses the requests library, which does not support asyncio,
    # this workaround is necessary to get issue multiple requests in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, go, task) for task in tasks]

    for _ in await asyncio.gather(*futures):
        pass
