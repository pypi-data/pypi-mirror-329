import argparse
from uuid import UUID

from .cli_client import create_client


def run(args: argparse.Namespace) -> None:
    version_number = args.version_number
    change_id = args.change_id

    print(create_client().delete_change(version_number, change_id))


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("delete-change", help="Delete selected change.")
    parser.add_argument("version_number", help="'major.minor.patch'")
    parser.add_argument("change_id", type=UUID)

    parser.set_defaults(func=run)
