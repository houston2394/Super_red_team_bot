import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from plugins.loader import PluginLoader


class TestPluginLoader(unittest.TestCase):
    def setUp(self):
        self.loader = PluginLoader("plugins")

    def test_loader_initializes(self):
        self.assertIsNotNone(self.loader)
        self.assertEqual(self.loader.plugin_dir, "plugins")

    def test_discover_plugins(self):
        plugins = self.loader.discover()
        self.assertIsInstance(plugins, list)

    def test_load_example_plugin(self):
        plugin = self.loader.load("example_plugin")
        self.assertIsNotNone(plugin)
        self.assertTrue(hasattr(plugin, "run"))

    def test_load_nonexistent_plugin_returns_none(self):
        plugin = self.loader.load("nonexistent_plugin_xyz")
        self.assertIsNone(plugin)


if __name__ == "__main__":
    unittest.main()
