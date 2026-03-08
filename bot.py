#!/usr/bin/env python3
"""
Super_red_team_bot - Main Entry Point
Orchestrates red team automation tasks through plugin system
"""

import os
import sys
import argparse
import configparser
from typing import Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

from plugins.loader import PluginLoader


class RedTeamBot:
    """
    Main bot orchestrator for red team operations
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the Red Team Bot

        Args:
            config_file: Path to configuration file (default: config/sample_config.ini)
        """
        # Load environment variables
        load_dotenv()

        # Initialize configuration
        self.config_file = config_file or "config/sample_config.ini"
        self.config = self._load_config()

        # Initialize plugin loader
        plugin_dir = "plugins"
        self.plugin_loader = PluginLoader(plugin_dir)

        # Initialize state
        self.loaded_plugins = {}
        self.results = {}

        print(f"[RedTeamBot] Initialized with config: {self.config_file}")

    def _load_config(self) -> configparser.ConfigParser:
        """
        Load configuration from INI file

        Returns:
            ConfigParser object with configuration
        """
        config = configparser.ConfigParser()

        if os.path.exists(self.config_file):
            config.read(self.config_file)
            print(f"[RedTeamBot] Loaded config from {self.config_file}")
        else:
            print(
                f"[RedTeamBot] Config file not found: {self.config_file}, using defaults"
            )
            # Set defaults
            config["general"] = {"log_level": "INFO", "output_dir": "recon/"}
            config["recon"] = {
                "endpoints_file": "recon/endpoints.json",
                "params_file": "recon/params.json",
            }
            config["plugins"] = {"enabled": ""}

        return config

    def load_plugins(self, plugin_names: Optional[List[str]] = None) -> int:
        """
        Load specified plugins or all enabled plugins from config

        Args:
            plugin_names: Optional list of plugin names to load

        Returns:
            Number of plugins successfully loaded
        """
        if plugin_names is None:
            # Load from config
            enabled_str = self.config.get("plugins", "enabled", fallback="")
            if enabled_str:
                plugin_names = [p.strip() for p in enabled_str.split(",") if p.strip()]
            else:
                # Discover all plugins
                plugin_names = self.plugin_loader.discover()

        count = 0
        for name in plugin_names:
            plugin = self.plugin_loader.load(name)
            if plugin:
                self.loaded_plugins[name] = plugin
                count += 1
                print(f"[RedTeamBot] Loaded plugin: {name}")
            else:
                print(f"[RedTeamBot] Failed to load plugin: {name}")

        print(f"[RedTeamBot] Loaded {count}/{len(plugin_names)} plugins")
        return count

    def run_plugin(self, plugin_name: str, **kwargs) -> Optional[Dict]:
        """
        Execute a specific plugin

        Args:
            plugin_name: Name of the plugin to execute
            **kwargs: Arguments to pass to the plugin

        Returns:
            Plugin execution result or None if failed
        """
        if plugin_name not in self.loaded_plugins:
            plugin = self.plugin_loader.load(plugin_name)
            if plugin:
                self.loaded_plugins[plugin_name] = plugin
            else:
                print(f"[RedTeamBot] Plugin not found: {plugin_name}")
                return None

        print(f"[RedTeamBot] Executing plugin: {plugin_name}")
        result = self.plugin_loader.execute(plugin_name, **kwargs)

        if result:
            self.results[plugin_name] = result
            print(f"[RedTeamBot] Plugin '{plugin_name}' completed")
        else:
            print(f"[RedTeamBot] Plugin '{plugin_name}' failed")

        return result

    def run_all_plugins(self, **kwargs) -> Dict[str, any]:
        """
        Execute all loaded plugins

        Args:
            **kwargs: Arguments to pass to each plugin

        Returns:
            Dictionary mapping plugin names to their results
        """
        print(f"[RedTeamBot] Running {len(self.loaded_plugins)} plugins")

        for plugin_name in self.loaded_plugins:
            self.run_plugin(plugin_name, **kwargs)

        return self.results

    def get_results(self) -> Dict[str, any]:
        """
        Get all plugin execution results

        Returns:
            Dictionary of results
        """
        return self.results

    def save_results(self, output_file: str) -> None:
        """
        Save results to a file

        Args:
            output_file: Path to output file (JSON format)
        """
        import json

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"[RedTeamBot] Results saved to {output_file}")


def main():
    """
    Command-line interface for the bot
    """
    parser = argparse.ArgumentParser(
        description="Super_red_team_bot - Red Team Automation Toolkit"
    )

    parser.add_argument(
        "--config",
        "-c",
        help="Path to configuration file",
        default="config/sample_config.ini",
    )

    parser.add_argument("--plugin", "-p", help="Run specific plugin", default=None)

    parser.add_argument(
        "--plugins", help="Comma-separated list of plugins to load", default=None
    )

    parser.add_argument(
        "--target",
        "-t",
        help="Target URL or identifier",
        default=os.getenv("TARGET_BASE_URL", "https://example.com"),
    )

    parser.add_argument(
        "--output", "-o", help="Output file for results (JSON)", default=None
    )

    parser.add_argument(
        "--list-plugins", help="List available plugins and exit", action="store_true"
    )

    parser.add_argument(
        "--verbose", "-v", help="Enable verbose output", action="store_true"
    )

    args = parser.parse_args()

    # Initialize bot
    bot = RedTeamBot(config_file=args.config)

    # List plugins if requested
    if args.list_plugins:
        print("\n[RedTeamBot] Available plugins:")
        plugins = bot.plugin_loader.discover()
        for plugin_name in plugins:
            print(f"  - {plugin_name}")
        return 0

    # Load plugins
    if args.plugins:
        plugin_list = [p.strip() for p in args.plugins.split(",")]
        bot.load_plugins(plugin_list)
    else:
        bot.load_plugins()

    # Execute plugins
    kwargs = {"target": args.target, "verbose": args.verbose}

    if args.plugin:
        # Run single plugin
        result = bot.run_plugin(args.plugin, **kwargs)
        if result:
            print(f"\n[RedTeamBot] Plugin result: {result}")
    else:
        # Run all loaded plugins
        results = bot.run_all_plugins(**kwargs)
        print(f"\n[RedTeamBot] Completed {len(results)} plugins")

    # Save results if output file specified
    if args.output:
        bot.save_results(args.output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
