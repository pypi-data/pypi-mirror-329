# Qore Client

Qore Client is a Python client library for the Qore API.

## Prerequisites

First, install `uv` package installer:

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows PowerShell
(Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing).Content | pwsh -Command -
```

## Installation

For users, simply install using pip:

```bash
pip install qore-client
```

## Development Environment Setup

1. Clone the repository

```bash
git clone <repository-url>
```

2. Create a virtual environment and install dependencies

```bash
bash dev.sh
```

## Testing Development Versions

```bash
# Install the package from TestPyPI
uv pip install -i https://test.pypi.org/simple/ qore-client=={version}

# Install the package from PyPI
uv pip install qore-client=={version}
```

## CI/CD

This project supports automated testing and deployment through GitLab CI/CD.