from contextlib import suppress

import requests
from realerikrani.baseclient import BaseAdapter, BaseClient
from realerikrani.projectclient import JWTAuth, cli_config

from .client import ChangelogClient


def create_client() -> ChangelogClient:
    config, _ = cli_config.read_config()
    adapter = BaseAdapter()
    with requests.Session() as session:
        jwt_auth = None
        with suppress(KeyError):
            jwt_auth = JWTAuth(
                *cli_config.read_project_and_key_id(), cli_config.read_private_key()
            )
        baseclient = BaseClient(
            session=session,
            adapter=adapter,
            url=cli_config.read_url(config),
            auth=jwt_auth,
        )
        return ChangelogClient(baseclient)
