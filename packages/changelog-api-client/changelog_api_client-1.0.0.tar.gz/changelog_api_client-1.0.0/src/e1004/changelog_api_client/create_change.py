import argparse

from .cli_client import create_client


def run(args: argparse.Namespace) -> None:
    version_number = args.version_number
    kind = args.kind
    body = args.body
    author = args.author

    print(create_client().create_change(version_number, kind, body, author))


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("create-change", help="Create a new change.")
    parser.add_argument("version_number", help="'major.minor.patch'")
    parser.add_argument(
        "kind",
        choices=["added", "changed", "deprecated", "removed", "fixed", "security"],
    )
    parser.add_argument("body", help="description of what was changed")
    parser.add_argument("author", help="who made the change")

    parser.set_defaults(func=run)
