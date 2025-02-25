# aiotainer

[![codecov](https://codecov.io/gh/Thomas55555/aiotainer/graph/badge.svg?token=Hn1Qp8ZvOt)](https://codecov.io/gh/Thomas55555/aiotainer)
[![Python Versions](https://img.shields.io/pypi/pyversions/aiotainer)](https://pypi.org/project/aiotainer/)
[![License](https://img.shields.io/github/license/Thomas55555/aiotainer.svg)](LICENSE.md)

Asynchronous library to communicate with the Portainer API

## Quickstart

In order to use the library, you'll need to do some work yourself to get authentication
credentials. This depends a lot on the context (e.g. redirecting to use OAuth via web)
but should be easy to incorporate using Portainers's authentication examples. See
Portainers's [Authentication](https://docs.portainer.io/admin/settings/authentication) for details.

You will implement `AbstractAuth` to provide an access token. Your implementation
will handle any necessary refreshes. You can invoke the service with your auth implementation
to access the API.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]

For a first start you can run the `example.py`, by doing the following steps

- `git clone https://github.com/Thomas55555/aiotainer.git`
- `cd aiotainer`
- `poetry install`
- Enter your personal `client_id` and `client_secret` in the `_secrets.yaml` and rename it to `secrets.yaml`
- Run with `poetry run ./example.py`

## Contributing

This is an active open-source project. We are always open to people who want to use the code or contribute to it.
This Python project is fully managed using the [Poetry][poetry] dependency manager.

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

To update snapshots:

```bash
poetry run pytest --snapshot-update
```

[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com/
