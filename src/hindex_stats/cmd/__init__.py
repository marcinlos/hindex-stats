"""
This package contains commands exposed to the user.

Each module implementing a command should contain the following two functions:

    def register_parser(subparsers): ...

which defines the command interface (name, argument types etc.) by adding an
appropriate subparser, and

    def execute(args): ...

which carries out the command based on arguments received from the user.
"""
