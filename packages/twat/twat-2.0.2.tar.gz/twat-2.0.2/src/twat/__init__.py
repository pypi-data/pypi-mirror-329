"""twat plugin host"""

from __future__ import annotations

import sys
from importlib import metadata
from typing import TYPE_CHECKING, Any, NoReturn

if TYPE_CHECKING:
    from types import ModuleType

__version__ = metadata.version(__name__)

# Enable package-style imports for plugins
__path__ = []
__package__ = "twat"


def _load_plugin(name: str) -> ModuleType | None:
    """Load a plugin by name."""
    try:
        eps = metadata.entry_points(group="twat.plugins")
        for ep in eps:
            if ep.name == name:
                plugin = ep.load()
                # Register the plugin in sys.modules
                plugin_name = f"twat.{name}"
                sys.modules[plugin_name] = plugin
                return plugin
    except Exception:
        return None
    return None


def __getattr__(name: str) -> Any:
    """Dynamic attribute lookup for plugins.

    To register a plugin, add the following to your pyproject.toml:

    [project.entry-points."twat.plugins"]
    hatch = "twat_hatch"  # Just point to the module

    Args:
        name: Name of plugin to load

    Returns:
        Loaded plugin module

    Raises:
        AttributeError: If plugin cannot be found or loaded
    """
    plugin = _load_plugin(name)
    if plugin is not None:
        return plugin

    msg = f"module '{__name__}' has no attribute '{name}'"
    raise AttributeError(msg)


def run_plugin(plugin_name: str) -> NoReturn:
    """Run a plugin's main function."""
    try:
        eps = metadata.entry_points(group="twat.plugins")
        for ep in eps:
            if ep.name == plugin_name:
                plugin = ep.load()
                if hasattr(plugin, "main"):
                    plugin.main()
                    sys.exit(0)
                else:
                    sys.exit(1)
    except Exception:
        sys.exit(1)

    sys.exit(1)


def main() -> NoReturn:
    """Main entry point."""
    if len(sys.argv) < 2:
        sys.exit(1)

    plugin_name = sys.argv[1]
    # Remove the plugin name from argv so the plugin sees the correct args
    sys.argv = [f"twat.{plugin_name}"] + sys.argv[2:]
    run_plugin(plugin_name)
