# fair-proxy-api

[![PyPI - Version](https://img.shields.io/pypi/v/fair-proxy-api.svg)](https://pypi.org/project/fair-proxy-api)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fair-proxy-api.svg)](https://pypi.org/project/fair-proxy-api)
[![CI](https://github.com/DataArtifex/fair-proxy-api/actions/workflows/test.yml/badge.svg)](https://github.com/DataArtifex/fair-proxy-api/actions/workflows/test.yml)
[![License](https://img.shields.io/github/license/DataArtifex/fair-proxy-api.svg)](https://github.com/DataArtifex/fair-proxy-api/blob/main/LICENSE.txt)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
[![DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/DataArtifex/fair-proxy-api)

**This project is in its early development stages. Stability is not guaranteed, and documentation is limited. We welcome your feedback and contributions.**

## Overview

This project is about Foo and Bar...


## Bootstrapping a New Project

If you are using this repository as a template, run the included rename script to set your project and package names:

```bash
./rename.sh "my-project-name" "my_package_name"
```

2. **Register with DeepWiki**: To ensure your documentation is indexed and discoverable by AI agents, register your new repository at [DeepWiki.com](https://deepwiki.com/).

## Installation

This project recommends using [uv](https://github.com/astral-sh/uv) for fast and reliable Python package management.

### Using uv (Recommended)

To set up the development environment with `uv`:

```bash
# Install dependencies and create virtual environment
uv sync
```

### Using Hatch

You can also use [Hatch](https://hatch.pypa.io/) directly:

```bash
# Run tests
hatch run test

# Enter the default shell
hatch shell
```

### Local Installation

For traditional installation:

```bash
pip install -e .
```


## Development

### Version Management
Versions are managed dynamically in `src/dartfx/fairproxy_api/__about__.py`. You can use `hatch version` to view or bump the version.

### Secret Management
For local development, create a `.env` file in the root directory. This file is git-ignored and can be used to store local API keys or configuration. These are automatically loaded by the test suite.

### Running Tests
```bash
uv run pytest
```

### Building Documentation
```bash
hatch run docs:build
```



## Usage

...

## Roadmap

...

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines and information on how to get started.
