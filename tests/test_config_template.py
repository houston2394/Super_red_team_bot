import unittest
import os

class TestConfigTemplates(unittest.TestCase):
    def test_sample_config_exists(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(project_root, 'config', 'sample_config.ini')
        self.assertTrue(os.path.exists(config_path), "Sample config template missing.")

if __name__ == '__main__':
    unittest.main()
