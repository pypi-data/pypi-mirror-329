import argparse
from uuid import UUID

from .cli_client import create_client


def run(args: argparse.Namespace) -> None:
    to_version_number = args.to_version_number
    from_version_number = args.from_version_number
    change_id = args.change_id
    print(
        create_client().move_change_to_other_version(
            from_version_number, to_version_number, change_id
        )
    )


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "move-change", help="Move change from one unreleased version to other one."
    )
    parser.add_argument("from_version_number", help="'major.minor.patch'")
    parser.add_argument("to_version_number", help="'major.minor.patch'")
    parser.add_argument("change_id", type=UUID)

    parser.set_defaults(func=run)
