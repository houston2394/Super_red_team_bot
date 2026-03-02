import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bot import RedTeamBot


class TestRedTeamBot(unittest.TestCase):
    def test_bot_initializes(self):
        bot = RedTeamBot()
        self.assertIsNotNone(bot)

    def test_bot_loads_config(self):
        bot = RedTeamBot()
        self.assertIsNotNone(bot.config)

    def test_bot_has_plugin_loader(self):
        bot = RedTeamBot()
        self.assertIsNotNone(bot.plugin_loader)


if __name__ == "__main__":
    unittest.main()
