import unittest
import json
import os

class TestReconOutputs(unittest.TestCase):
    def setUp(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.endpoints_path = os.path.join(project_root, 'recon', 'endpoints.json')
        self.params_path = os.path.join(project_root, 'recon', 'params.json')

    def test_endpoints_json_format(self):
        if not os.path.exists(self.endpoints_path):
            self.skipTest("endpoints.json not found")
        with open(self.endpoints_path) as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        for entry in data:
            self.assertIn('url', entry)
            self.assertIn('method', entry)
            self.assertIn('auth_required', entry)
            self.assertIn('parameters', entry)

    def test_params_json_format(self):
        if not os.path.exists(self.params_path):
            self.skipTest("params.json not found")
        with open(self.params_path) as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        for entry in data:
            self.assertIn('param', entry)
            self.assertIn('location', entry)

if __name__ == '__main__':
    unittest.main()
