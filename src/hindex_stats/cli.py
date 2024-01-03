import argparse
import argcomplete


def run(args):
    pass


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="Actions", dest="action")

    subparsers.add_parser("command", help="...")

    # ...

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
