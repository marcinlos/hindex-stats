import itertools

from hindex_stats.utils import take, SkipOnce
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
        if author.email is not None:
            print(f"  e-mail: {author.email}")
        if author.hindex is not None:
            print(f"  h-index: {author.hindex}")
        if author.interests:
            print(f"  interests: {', '.join(author.interests)}")
        print(f"  citations: {author.citations}")
