"""
This package contains commands exposed to the user.

Each module implementing a command should contain a function

    def register_parser(subparsers): ...

which defines the command interface (name, argument types etc.) by
adding an appropriate subparser:

    cmd_parser = subparsers.add_parser("command-name", ...)
    cmd_parser.add_argument(...)

and sets the command handler:

    cmd_parser.set_defaults(handler=CMD_HANDLER)

where CMD_HANDLER is a callable that carries out the command based on
arguments received from the user. The handler is later invoked with the
result of parse_args() call.
"""
