import itertools

from hindex_stats.utils import take, SkipOnce
from hindex_stats.author import Author
import hindex_stats.fetch as fetch


def register_parser(subparsers):
    p = subparsers.add_parser("show", help="show dupa")
    p.add_argument("query", type=str)
    p.add_argument(
        "-n", "--max-results", help="maximum number of results", type=int, default=5
    )


def execute(args):
    separator = SkipOnce(print)
    for author in take(args.max_results, fetch.search(args.query)):
        separator()
        print(f"{author.name}")
        print(f"  {author.affiliation}")
        print(f"  h-index: {author.hindex}")
        print(f"  {', '.join(author.interests)}")
