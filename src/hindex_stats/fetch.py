import concurrent.futures
import asyncio
from dataclasses import dataclass
from typing import Callable, Iterable

from scholarly import scholarly

from hindex_stats.utils import take
from hindex_stats.data import AuthorEntry


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


def search(query: str):
    for result in scholarly.search_author(query):
        author = scholarly.fill(result, sections=["indices"])
        yield _author_entry_from_dict(author)


@dataclass
class QueryTask:
    query: str
    max_results: int
    callback: Callable


async def execute_queries(tasks: Iterable[QueryTask], threads: int):
    def go(task):
        for item in take(task.max_results, search(task.query)):
            task.callback(item)

    # Since scholarly uses the requests library, which does not support asyncio,
    # this workaround is necessary to get issue multiple requests in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        loop = asyncio.get_event_loop()
        futures = [loop.run_in_executor(executor, go, task) for task in tasks]

    for _ in await asyncio.gather(*futures):
        pass
