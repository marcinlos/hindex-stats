import itertools

from hindex_stats.utils import take, SkipOnce
from hindex_stats.data import Query
import hindex_stats.fetch as fetch


def register_parser(subparsers):
    p = subparsers.add_parser("show", help="show dupa")
    p.add_argument("name", type=str, help="author name")
    p.add_argument("affiliation", type=str, help="author affiliation", nargs="?")
    p.add_argument(
        "-n", "--max-results", help="maximum number of results", type=int, default=5
    )


def _build_query(args) -> Query:
    return Query(args.name, args.affiliation)


def execute(args):
    query = _build_query(args)

    separator = SkipOnce(print)
    for author in take(args.max_results, fetch.search(query)):
        separator()
        print(f"{author.name}")
        print(f"  {author.affiliation}")
        if author.email is not None:
            print(f"  e-mail: {author.email}")
        if author.hindex is not None:
            print(f"  h-index: {author.hindex}")
        if author.interests:
            print(f"  interests: {', '.join(author.interests)}")
        print(f"  citations: {author.citations}")
