# 🎯 Typer Common Functions

Helper functions for [Typer](https://typer.tiangolo.com/) CLI applications.

[![PyPI version](https://badge.fury.io/py/typer-common-functions.svg)](https://pypi.org/project/typer-common-functions/)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Python Versions](https://img.shields.io/pypi/pyversions/typer-common-functions.svg)](https://pypi.org/project/typer-common-functions/)

## ✨ Features

- 📝 Rich-based logging configuration
- ⚡ Typer helper functions and utilities

## 📦 Installation

Available on [PyPI](https://pypi.org/project/typer-common-functions/):

```bash
pip install typer-common-functions
```

## 🚀 Usage

```python
from typer_common_functions import set_logging, typer_unpacker

# Configure logging with Rich
set_logging(verbose=True)

# Create CLI commands with type hints
@typer_unpacker
def hello(name: str) -> str:
    return f"Hello {name}!"
```

## 🛠️ Development

### 📋 Requirements

- 🐍 Python 3.8+
- 🏗️ [Hatch](https://hatch.pypa.io/) for project management
- ⚡ [UV](https://github.com/astral-sh/uv) for dependency management
- 🐳 [Dev Container](https://containers.dev/) support (optional)

### ⚙️ Setup

```bash
# Install tools
uv pip install hatch pre-commit
pre-commit install

# Create dev environment
hatch shell

# Run tests
hatch run dev:test

# Run linting
hatch run dev:lint

# Run formatters
hatch run dev:format
```

### 🔍 Code Quality

- ✅ Testing: pytest with coverage
- 🔬 Linting: flake8, pylint, mypy
- 🎨 Formatting: black, isort
- 🛡️ Security: bandit
- 🔄 Git hooks: pre-commit

### 📦 Release Process

1. 🔖 Run "Version Bump" workflow in GitHub Actions
2. 🎯 Choose version bump type
3. 👀 Review and merge the created PR
4. 🚀 Automated release and PyPI publish on merge

## 📄 License

LGPL-3.0-or-later - see [LICENSE](LICENSE)
