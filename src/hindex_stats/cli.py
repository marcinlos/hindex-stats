from importlib import import_module
import sys
import argparse
import argcomplete


COMMANDS = [
    "show",
]


def load_command_module(cmd):
    module_name = "hindex_stats.cmd." + cmd
    module = import_module(module_name)
    return module


def build_cmd_parsers(subparsers, command_modules):
    for cmd, module in command_modules.items():
        module.register_parser(subparsers)


def run(args, command_modules):
    command = args.action
    module = command_modules[command]
    module.execute(args)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Actions", dest="action")

    command_modules = {cmd: load_command_module(cmd) for cmd in COMMANDS}
    build_cmd_parsers(subparsers, command_modules)

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    run(args, command_modules)


if __name__ == "__main__":
    main()
