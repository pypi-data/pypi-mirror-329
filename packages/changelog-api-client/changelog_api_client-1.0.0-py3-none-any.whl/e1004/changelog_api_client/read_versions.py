import argparse

from .cli_client import create_client


def run(args: argparse.Namespace) -> None:
    page_size = args.page_size
    page_token = args.page_token

    print(create_client().read_versions(page_size, page_token))


def add_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser("read-versions", help="Read existing versions.")
    parser.add_argument(
        "page_size", type=int, help="number of versions per page'", default=None
    )
    parser.add_argument("page_token", help="Token for pagination", default=None)

    parser.set_defaults(func=run)
