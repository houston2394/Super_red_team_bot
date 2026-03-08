import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from recon.fuzzer import ParameterFuzzer


class TestParameterFuzzer(unittest.TestCase):
    def test_fuzzer_initializes(self):
        fuzzer = ParameterFuzzer("https://example.com/api")
        self.assertIsNotNone(fuzzer)
        self.assertEqual(fuzzer.target_url, "https://example.com/api")

    def test_common_params_exist(self):
        fuzzer = ParameterFuzzer("https://example.com/api")
        self.assertIsInstance(fuzzer.common_params, list)
        self.assertGreater(len(fuzzer.common_params), 0)

    def test_fuzz_payloads_exist(self):
        fuzzer = ParameterFuzzer("https://example.com/api")
        self.assertIsInstance(fuzzer.fuzz_payloads, list)
        self.assertGreater(len(fuzzer.fuzz_payloads), 0)


if __name__ == "__main__":
    unittest.main()
