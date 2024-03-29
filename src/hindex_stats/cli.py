import argparse
from importlib import import_module

import argcomplete

COMMANDS = [
    "show",
]


def load_command_module(cmd):
    module_name = "hindex_stats.cmd." + cmd
    module = import_module(module_name)
    return module


def build_cmd_parsers(subparsers, command_modules):
    for module in command_modules:
        module.register_parser(subparsers)


def run(args):
    command = args.handler
    command(args)


def package_version():
    import importlib.metadata as meta

    return meta.version("hindex-stats")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version",
        help="print version information",
        action="version",
        version=f"%(prog)s {package_version()}",
    )
    subparsers = parser.add_subparsers(title="Actions", dest="action")

    command_modules = [load_command_module(cmd) for cmd in COMMANDS]
    build_cmd_parsers(subparsers, command_modules)

    # handles a call with no command
    parser.set_defaults(handler=lambda _: parser.print_help())

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
