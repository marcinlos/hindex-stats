import concurrent.futures
import asyncio
from dataclasses import dataclass
from typing import Callable, Iterable

from scholarly import scholarly

from hindex_stats.utils import take
from hindex_stats.author import Author


def _make_profile_link(img_link: str) -> str:
    return img_link.replace("view_op=medium_photo&", "")


def _author_from_dict(data: dict) -> Author:
    return Author(
        name=data["name"],
        affiliation=data["affiliation"],
        interests=data["interests"],
        hindex=data["hindex"],
        profile=_make_profile_link(data["url_picture"]),
    )


def search(query: str):
    for result in scholarly.search_author(query):
        author = scholarly.fill(result, sections=["indices"])
        yield _author_from_dict(author)


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
