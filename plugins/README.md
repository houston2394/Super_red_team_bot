# Plugin Development Guide

To add a new plugin to Super_red_team_bot:

1. Place your plugin script/module in this directory.
2. Follow the template below for consistency:

---

## Plugin Template (Python Example)

"""
Plugin Name: <plugin_name>
Description: <short description>
"""

def run(*args, **kwargs):
    # Plugin logic here
    pass

---

## Guidelines
- Document the plugin's purpose and usage at the top of the file.
- Ensure the plugin exposes a `run()` function as the entry point.
- Add any dependencies to the project documentation.

## Loading Plugins
Plugins listed in the config file under `[plugins] enabled` will be loaded automatically.

## Example
See `sample_plugin.py` for a reference implementation.
