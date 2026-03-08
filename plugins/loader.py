"""
Dynamic Plugin Loader
Discovers and loads plugins from the plugins directory
"""

import os
import importlib
import sys
from typing import Optional, List, Any


class PluginLoader:
    """
    Dynamically loads and manages plugins
    """

    def __init__(self, plugin_dir: str = "plugins"):
        """
        Initialize the plugin loader

        Args:
            plugin_dir: Directory containing plugin modules
        """
        self.plugin_dir = plugin_dir
        self.loaded_plugins = {}

        # Add plugin directory to Python path
        abs_plugin_dir = os.path.abspath(plugin_dir)
        parent_dir = os.path.dirname(abs_plugin_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)

    def discover(self) -> List[str]:
        """
        Discover available plugins in the plugin directory

        Returns:
            List of plugin names (without .py extension)
        """
        if not os.path.exists(self.plugin_dir):
            return []

        plugins = []
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                plugin_name = filename[:-3]
                if plugin_name in ("loader", "__init__"):
                    continue
                plugins.append(plugin_name)


        return plugins

    def load(self, plugin_name: str) -> Optional[Any]:
        """
        Load a specific plugin by name

        Args:
            plugin_name: Name of the plugin module (without .py)

        Returns:
            Loaded plugin module or None if loading fails
        """
        if plugin_name in self.loaded_plugins:
            return self.loaded_plugins[plugin_name]

        try:
            # Import the plugin module
            module_path = f"plugins.{plugin_name}"
            plugin_module = importlib.import_module(module_path)

            # Validate plugin has required interface
            if not hasattr(plugin_module, "run"):
                print(f"Warning: Plugin '{plugin_name}' missing 'run' function")
                return None

            self.loaded_plugins[plugin_name] = plugin_module
            return plugin_module

        except ImportError as e:
            print(f"Error loading plugin '{plugin_name}': {e}")
            return None
        except Exception as e:
            print(f"Unexpected error loading plugin '{plugin_name}': {e}")
            return None

    def load_all(self) -> dict:
        """
        Load all discovered plugins

        Returns:
            Dictionary mapping plugin names to loaded modules
        """
        discovered = self.discover()
        for plugin_name in discovered:
            self.load(plugin_name)

        return self.loaded_plugins

    def execute(self, plugin_name: str, *args, **kwargs) -> Any:
        """
        Execute a plugin's run function

        Args:
            plugin_name: Name of the plugin to execute
            *args: Positional arguments for the plugin
            **kwargs: Keyword arguments for the plugin

        Returns:
            Result of the plugin execution or None if execution fails
        """
        plugin = self.load(plugin_name)
        if plugin is None:
            print(f"Cannot execute plugin '{plugin_name}': not loaded")
            return None

        try:
            return plugin.run(*args, **kwargs)
        except Exception as e:
            print(f"Error executing plugin '{plugin_name}': {e}")
            return None
