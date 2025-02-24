# Changelog-API-Client

Use <https://github.com/e1004/Changelog-API> more easily!

## CLI

After installing, run `changelog -h` to see available commands.

Before creating a changelog, run `cli_project -h` to see available commands to create project.

Set `PROJECT_CLI_CONFIG_PATH` environment variable.
The config file must be in ini-format with url of your Changelog API.

```ini
[DEFAULT]
url = http://localhost:5000
```

## API Client

Import the client with `from e1004.changelog_api_client import ChangelogClient`

## Direct Dependances

- [requests](https://github.com/psf/requests) Licensed under [Apache License 2.0](./LICENSE)
- [realerikrani-baseclient](https://github.com/realerikrani/baseclient) Licensed under [Apache License 2.0](./LICENSE)
- [realerikrani-projectclient](https://github.com/realerikrani/projectclient) Licensed under [Apache License 2.0](./LICENSE)
