# Changelog

## [v1.4.1] - 2025-02-22

Minor release to fix import errors caused by a missing dependency in [v1.4.0].

### Added

- Missing cryptography dependency to `pyproject.toml` ([`0e63a2b`](https://github.com/fedamerd/msgraph-py/commit/0e63a2b))

### Removed

- `requirements.txt` (obsolete) ([`063a0a0`](https://github.com/fedamerd/msgraph-py/commit/063a0a0))
- Broken links to function descriptions in `README.md` ([`f04cc94`](https://github.com/fedamerd/msgraph-py/commit/f04cc94))

## [v1.4.0] - 2025-02-17

This release implements certificate-based authentication as an alternative to using a static client secret. This authentication method works by creating and using a signed, short-lived JWT assertion to authenticate the client to the OpenID provider.

The benefits of this authentication method are:

- The clients private key is never shared with anyone. The OpenID provider only needs to known the corresponding public certificate to validate the clients JWT assertions.
- A signed JWT is only valid for 30 seconds and cannot be replayed, thus greatly reducing the risks of token theft or secrets being compromised.

For more information on how to use certificate-based authentication, see the [README.md](https://github.com/fedamerd/msgraph-py/blob/main/README.md#certificate-based-authentication)

### Added

- Support for client assertion authentication method ([`007bf54`](https://github.com/fedamerd/msgraph-py/commit/007bf54))

## [v1.3.1] - 2024-11-27

This minor release aims to fix an unintended change to the default HTTP request timeout threshold after migrating to the `httpx` backend in [v1.2.0], which set a timeout of 5 seconds as the client default. This caused timeouts for certain long-running queries (e.g. `/auditLogs/signIns/`).

The default timeout has now been increased to **30 seconds**, in addition to adding an optional `timeout` parameter to every functions for overriding this value when needed.

Setting the value to `None` will disable timeout entirely. This was the previous behaviour before [v1.2.0] and is not recommended. Timeouts will cause an `httpx.TimeoutException` and should be handled by the application logic.

### Added

- Optional `timeout` parameter per function for overriding the default global timeout value ([`32f6a29`](https://github.com/fedamerd/msgraph-py/commit/32f6a29))

### Fixed

- Low timeout value after migrating to httpx. Default has been increased to 30 seconds ([`2790a36`](https://github.com/fedamerd/msgraph-py/commit/2790a36))

## [v1.3.0] - 2024-11-25

This release adds two new functions to the devices module for retrieving BitLocker recovery keys.

For more information on the `bitlockerRecoveryKey` resource type and examples, see [Microsofts API documentation](https://learn.microsoft.com/en-us/graph/api/resources/bitlockerrecoverykey?view=graph-rest-1.0).

### Added

- `get_bitlocker_key()` - returns BitLocker recovery keys based on a key ID or a filter query ([`4738200`](https://github.com/fedamerd/msgraph-py/commit/4738200))
- `get_device_bitlocker_key()` - returns BitLocker recovery keys based on a device ID, as a simple convenience function ([`4738200`](https://github.com/fedamerd/msgraph-py/commit/4738200))

## [v1.2.0] - 2024-11-24

This release changes the underlying Python HTTP library from `requests` to `httpx` and improves performance by enabling connection pooling and HTTP/2 support. All functions now share the same HTTP client internally.

This should reduce latency by avoiding establishing new connections on every request, which is important when sending multiple consecutive API requests in a loop.

### Added

- Connection pooling for HTTP requests ([`03636eb`](https://github.com/fedamerd/msgraph-py/commit/03636eb))
- HTTP/2 support ([`03636eb`](https://github.com/fedamerd/msgraph-py/commit/03636eb))

### Changed

- HTTP library from `requests` to `httpx` ([`03636eb`](https://github.com/fedamerd/msgraph-py/commit/03636eb))
- GitHub Actions CI/CD `release.yml` workflow updated based on the latest Python Packaging User Guide ([`27cda40`](https://github.com/fedamerd/msgraph-py/commit/27cda40))

## [v1.1.0] - 2024-03-03

This release adds two new functions to the devices module.

### Added

- `list_owned_devices()` - returns a users owned devices in Entra ID ([`38ac9e1`](https://github.com/fedamerd/msgraph-py/commit/38ac9e1))
- `get_laps_password()` - returns the decoded LAPS password for a device ([`05943a8`](https://github.com/fedamerd/msgraph-py/commit/05943a8))
- Project URLs to `pyproject.toml` ([`cc8ac00`](https://github.com/fedamerd/msgraph-py/commit/cc8ac00))

### Changed

- List of functions in `README.md` now links to the corresponding Python modules ([`b5e158a`](https://github.com/fedamerd/msgraph-py/commit/b5e158a))

### Fixed

- Wrong return type hint in `list_group_members()` ([`0a95c48`](https://github.com/fedamerd/msgraph-py/commit/0a95c48))

## [v1.0.0] - 2024-02-21

First public release of **`msgraph-py`** – a Python package providing API wrappers to simplify interaction with Microsoft Graph API.

### Features

- Automatic caching and renewal of access tokens, avoiding unnecessary API-calls.
- Sets the correct headers and parameters for you when required (advanced queries).
- Pages results automatically when retrieving large datasets.
- Useful logging and error messages with the Python logging module.
- Optional integration with Django settings.py for reading environment variables.

### Installation

Releases are also published to [PyPI](https://pypi.org/project/msgraph-py/) and can be installed with the following command:

```console
python -m pip install msgraph-py
```

See the [README](https://github.com/fedamerd/msgraph-py/blob/main/README.md) for more information on how to get started, as well as usage examples.

### Contribute

Found a bug or want to request a feature? Open a new issue using the [issue tracker](https://github.com/fedamerd/msgraph-py/issues).

[v1.4.1]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.4.1
[v1.4.0]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.4.0
[v1.3.1]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.3.1
[v1.3.0]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.3.0
[v1.2.0]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.2.0
[v1.1.0]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.1.0
[v1.0.0]: https://github.com/fedamerd/msgraph-py/releases/tag/v1.0.0
