# 🎯 Typer Common Functions

Some Helpful Functions around the wonderful CLI Library [Typer](https://typer.tiangolo.com/)

[![PyPI version](https://badge.fury.io/py/typer-common-functions.svg)](https://badge.fury.io/py/typer-common-functions)
[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Python Versions](https://img.shields.io/pypi/pyversions/typer-common-functions.svg)](https://pypi.org/project/typer-common-functions/)

## ✨ Features

- 📝 **Logging Setup**: Easy configuration of Rich-based logging
- ⚡ **Typer Utilities**: Helper functions for Typer CLI applications
- 🐍 **Modern Python**: Type hints, dataclasses, and modern Python features
- ✅ **Well Tested**: Comprehensive test coverage
- 📚 **Well Documented**: Clear documentation and examples

## 📦 Installation

```bash
pip install typer-common-functions
```

## 🚀 Quick Start

```python
from typer_common_functions.logging import set_logging
from typer_common_functions.typer import typer_retuner, typer_unpacker

# Setup Rich logging
set_logging(verbose=True)

# Use typer helpers in your CLI
@typer_unpacker
def your_cli_command(name: str, verbose: bool = False):
    return f"Hello {name}!"
```

## 🛠️ Development

This project uses modern Python tooling:
- 🏗️ [Hatch](https://hatch.pypa.io/) for project management, building, and publishing
- 🚀 [UV](https://github.com/astral-sh/uv) for fast dependency management
- 🔍 [pre-commit](https://pre-commit.com/) for code quality
- 🔄 GitHub Actions for CI/CD
- 🐳 [Dev Container](https://containers.dev/) for consistent development environments

### 🐳 Development Container

The easiest way to get started is using the provided Dev Container:

1. Install [VS Code](https://code.visualstudio.com/) and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
2. Clone the repository
3. Open in VS Code and click "Reopen in Container" when prompted
4. The container will automatically:
   - Set up Python 3.12
   - Install UV and Hatch
   - Configure pre-commit hooks
   - Install VS Code extensions

### 🏁 Getting Started

There are two ways to get started:

#### 1️⃣ Using Dev Container (Recommended)

The easiest way is to use the Dev Container as described in the [Development Container](#-development-container) section above. Everything will be set up automatically.

#### 2️⃣ Manual Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/OpenJKSoftware/typer-common-functions.git
   cd typer-common-functions
   ```

2. Install development tools:
   ```bash
   # Using UV for faster installation
   uv pip install hatch pre-commit
   pre-commit install
   ```

3. Setup development environment:
   ```bash
   # Create and activate environment with Hatch
   hatch shell

   # Run tests (from project root)
   hatch run dev:test

   # Run linting
   hatch run dev:lint

   # Run formatters
   hatch run dev:format
   ```

> 💡 **Note**: Make sure to run commands from the project root directory. All commands use the `dev` environment defined in `pyproject.toml`.

### 🎯 Code Quality

We use several tools to ensure code quality:
- 🎨 **black**: Code formatting
- 📋 **isort**: Import sorting
- 🔍 **flake8**: Style guide enforcement
- 🎯 **mypy**: Static type checking
- 🔬 **pylint**: Code analysis
- ✅ **pytest**: Testing framework

All these checks run automatically on pull requests.

### 🚀 Release Process

We use GitHub Actions for automated version management and publishing:

1. **Creating a Release**:
   - Go to Actions → ["Version Bump"](.github/workflows/version-bump.yml) workflow
   - Click "Run workflow"
   - Choose version bump type (patch/minor/major/rc/beta/alpha)
   - A PR will be created with:
     - Version bump changes
     - Detailed changelog from commits
   - Review and merge the PR

2. **Automated Publishing**:
   - When the version bump PR is merged:
     - A new GitHub release is created
     - Package is published to PyPI

For detailed workflow documentation, see [🔄 GitHub Workflows](.github/workflows/README.md)

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

This project is licensed under the LGPL-3.0-or-later License - see the [LICENSE](LICENSE) file for details.
