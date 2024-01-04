import hindex_stats.fetch as fetch
from hindex_stats.data import InfoType, Query
from hindex_stats.utils import SkipOnce, flag_union, take


def register_parser(subparsers):
    p = subparsers.add_parser(
        "show",
        help="display information about researchers matching given query",
        description="""
        Display information about resears matching the specified name and affiliation,
        if specified.
        """,
    )
    p.add_argument("name", help="author name")
    p.add_argument("affiliation", nargs="?", help="author affiliation")
    p.add_argument(
        "-n",
        "--max-results",
        type=int,
        default=5,
        metavar="MAX",
        help="maximum number of results (default: %(default)s)",
    )

    p.add_argument(
        "--info",
        nargs="*",
        choices=("hindex",),
        metavar="TYPE",
        help="required types of information, one or more of: %(choices)s",
    )
    p.set_defaults(handler=execute)


def _build_query(args) -> Query:
    return Query(args.name, args.affiliation)


def _required_info(args) -> InfoType:
    name_to_flag = {"hindex": InfoType.HINDEX}
    flags = (name_to_flag[s] for s in args.info)
    return flag_union(flags, InfoType.NONE)


def execute(args):
    query = _build_query(args)
    info = _required_info(args)

    separator = SkipOnce(print)
    for author in take(args.max_results, fetch.search(query, info)):
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
