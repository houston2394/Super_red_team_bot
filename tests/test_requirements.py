import unittest
import os


class TestRequirements(unittest.TestCase):
    def test_requirements_file_exists(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        req_path = os.path.join(project_root, "requirements.txt")
        self.assertTrue(os.path.exists(req_path), "requirements.txt not found")

    def test_requirements_has_essential_packages(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        req_path = os.path.join(project_root, "requirements.txt")
        with open(req_path) as f:
            content = f.read()
        self.assertIn("requests", content)
        self.assertIn("beautifulsoup4", content)
        self.assertIn("pytest", content)

    def test_env_example_exists(self):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        env_path = os.path.join(project_root, ".env.example")
        self.assertTrue(os.path.exists(env_path), ".env.example not found")


if __name__ == "__main__":
    unittest.main()
