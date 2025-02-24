from argparse import ArgumentParser

from . import (
    create_change,
    create_version,
    delete_change,
    delete_version,
    move_change,
    read_changes,
    read_versions,
    release_version,
)


def main() -> None:
    parser = ArgumentParser(
        description="""CLI for Changelog API;
    before creating a changelog,
    create a project and its access key, execute 'cli_project -h'"""
    )

    subparsers = parser.add_subparsers(dest="command", required=True)
    create_version.add_parser(subparsers)
    delete_version.add_parser(subparsers)
    release_version.add_parser(subparsers)
    read_versions.add_parser(subparsers)
    create_change.add_parser(subparsers)
    delete_change.add_parser(subparsers)
    read_changes.add_parser(subparsers)
    move_change.add_parser(subparsers)

    args = parser.parse_args()
    args.func(args)
