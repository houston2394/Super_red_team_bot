import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from recon.scanner import EndpointScanner


class TestEndpointScanner(unittest.TestCase):
    def test_scanner_initializes(self):
        scanner = EndpointScanner("https://example.com")
        self.assertIsNotNone(scanner)
        self.assertEqual(scanner.base_url, "https://example.com")

    def test_scanner_normalizes_url(self):
        scanner = EndpointScanner("https://example.com/")
        self.assertEqual(scanner.base_url, "https://example.com")

    def test_common_paths_list_exists(self):
        scanner = EndpointScanner("https://example.com")
        self.assertIsInstance(scanner.common_paths, list)
        self.assertGreater(len(scanner.common_paths), 0)


if __name__ == "__main__":
    unittest.main()
