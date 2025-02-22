# twat

A plugin-based Python package system that provides a unified interface for various utilities.

## Features

- Plugin system for Python packages with standardized interfaces
- Dynamic plugin loading and discovery
- Modern Python packaging with PEP 621 compliance
- Type hints and runtime type checking
- Comprehensive test suite and documentation
- CI/CD ready configuration

## Installation

```bash
pip install twat
```

## Usage

### As a Library

```python
import twat

# Load a plugin
fs = twat.fs  # Loads the twat-fs plugin

# List available plugins
from importlib.metadata import entry_points
plugins = entry_points(group="twat.plugins")
```

### Command Line

```bash
# Run a plugin through the twat command
twat fs --help

# Or run the plugin directly if it provides a CLI
twat-fs --help
```

## Plugin Development Guide

To create a new plugin for the `twat` system, follow these guidelines. We'll use the `twat-fs` package as an example.

### 1. Package Structure

```
twat-yourplugin/
├── src/
│   └── twat_yourplugin/
│       ├── __init__.py      # Main package interface
│       ├── __main__.py      # CLI entry point
│       └── core.py          # Core functionality
├── tests/
├── pyproject.toml           # Package configuration
├── README.md
└── LICENSE
```

### 2. Package Configuration

Your `pyproject.toml` should include:

```toml
[project]
name = "twat-yourplugin"  # Use hyphen in package name
dependencies = [
    "twat",               # Always include the main package
    # Your other dependencies
]

[project.scripts]
twat-yourplugin = "twat_yourplugin.__main__:main"  # Optional CLI

[project.entry-points."twat.plugins"]
yourplugin = "twat_yourplugin"  # Register as a twat plugin
```

### 3. Package Interface

Your `__init__.py` should expose a clean public API:

```python
# this_file: src/twat_yourplugin/__init__.py
"""Package description."""

from importlib import metadata

__version__ = metadata.version(__name__)

# Export your public API
from .core import main_function, OtherClass

__all__ = ["main_function", "OtherClass"]
```

### 4. CLI Support (Optional)

If your plugin provides a command-line interface:

```python
# this_file: src/twat_yourplugin/__main__.py
"""Command-line interface."""

import sys
from typing import NoReturn

def main() -> NoReturn:
    """CLI entry point."""
    # Your CLI implementation
    sys.exit(0)

if __name__ == "__main__":
    main()
```

### 5. Example Implementation

Here's a minimal example based on `twat-fs`:

```python
# src/twat_yourplugin/__init__.py
"""Your plugin description."""

from importlib import metadata
from .core import upload_file, ProviderType

__version__ = metadata.version(__name__)
__all__ = ["upload_file", "ProviderType"]

# src/twat_yourplugin/__main__.py
"""CLI interface."""

import sys
from typing import NoReturn
import fire
from loguru import logger

from .core import upload_file

def main() -> NoReturn:
    """CLI entry point."""
    try:
        fire.Fire({
            "upload": upload_file,
            # other commands...
        })
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 6. Best Practices

1. **Naming**:
   - Package name: `twat-yourplugin` (with hyphen)
   - Import name: `twat_yourplugin` (with underscore)
   - Plugin entry point: `yourplugin` (no prefix)

2. **Dependencies**:
   - Always include `twat` as a dependency
   - Use optional dependencies for provider-specific features
   - Include development tools in `dev` extra

3. **Documentation**:
   - Include docstrings for all public APIs
   - Provide a comprehensive README
   - Include usage examples

4. **Testing**:
   - Write unit tests for core functionality
   - Include integration tests if applicable
   - Test both Python API and CLI interface

5. **Type Hints**:
   - Use type hints throughout your code
   - Support Python 3.10+
   - Follow PEP 484 and PEP 585

### 7. Development Workflow

```bash
# Create development environment
pip install hatch
hatch shell

# Install in development mode
pip install -e '.[dev,test]'

# Run tests
hatch run test
hatch run test-cov

# Run linting
hatch run lint

# Format code
hatch run format
```

## License

MIT License  
.
