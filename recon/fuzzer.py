import requests
import urllib3
from typing import List, Dict, Optional
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ParameterFuzzer:
    COMMON_PARAMS = [
        "id",
        "user_id",
        "userId",
        "uid",
        "name",
        "username",
        "user",
        "email",
        "mail",
        "token",
        "api_key",
        "key",
        "page",
        "limit",
        "offset",
        "search",
        "query",
        "q",
        "file",
        "path",
        "url",
        "redirect",
        "return",
        "next",
        "callback",
        "jsonp",
        "debug",
        "test",
        "dev",
        "admin",
        "role",
        "action",
        "cmd",
        "command",
        "sort",
        "order",
        "orderby",
        "format",
        "type",
        "data",
        "content",
        "body",
    ]

    FUZZ_PAYLOADS = [
        "1",
        "0",
        "-1",
        "999999",
        "test",
        "admin",
        "true",
        "false",
        "'",
        '"',
        "<>",
        "../",
        "${test}",
        "{{test}}",
        "",
        "null",
        "undefined",
    ]

    def __init__(
        self,
        target_url: str,
        timeout: int = 10,
        max_threads: int = 3,
        verify_ssl: bool = False,
    ):
        self.target_url = target_url
        self.timeout = timeout
        self.max_threads = max_threads
        self.verify_ssl = verify_ssl
        self.discovered_params = []
        self.common_params = self.COMMON_PARAMS.copy()
        self.fuzz_payloads = self.FUZZ_PAYLOADS.copy()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (RedTeam Fuzzer/1.0)"})
        self.baseline_response = None

    def get_baseline(self) -> Optional[requests.Response]:
        if self.baseline_response:
            return self.baseline_response
        try:
            response = self.session.get(
                self.target_url, timeout=self.timeout, verify=self.verify_ssl
            )
            self.baseline_response = response
            print(
                f"[*] Baseline: {response.status_code} ({len(response.content)} bytes)"
            )
            return response
        except Exception as e:
            print(f"[-] Error getting baseline: {e}")
            return None

    def fuzz_parameter(
        self, param_name: str, location: str = "query"
    ) -> Optional[Dict]:
        interesting_responses = []
        baseline = self.get_baseline()
        if not baseline:
            return None

        baseline_length = len(baseline.content)
        baseline_status = baseline.status_code

        for payload in self.fuzz_payloads:
            try:
                if location == "query":
                    params = {param_name: payload}
                    response = self.session.get(
                        self.target_url,
                        params=params,
                        timeout=self.timeout,
                        verify=self.verify_ssl,
                    )
                elif location == "body":
                    data = {param_name: payload}
                    response = self.session.post(
                        self.target_url,
                        data=data,
                        timeout=self.timeout,
                        verify=self.verify_ssl,
                    )
                else:
                    continue

                response_length = len(response.content)

                if response.status_code != baseline_status:
                    interesting_responses.append(
                        {
                            "payload": payload,
                            "status_code": response.status_code,
                            "reason": "status_code_change",
                        }
                    )
                    print(
                        f"[+] {param_name}={payload} → Status: {response.status_code}"
                    )
                elif abs(response_length - baseline_length) > baseline_length * 0.1:
                    interesting_responses.append(
                        {
                            "payload": payload,
                            "length_diff": response_length - baseline_length,
                            "reason": "length_change",
                        }
                    )
                    print(
                        f"[+] {param_name}={payload} → Length diff: {response_length - baseline_length}"
                    )
                elif any(
                    err in response.text.lower()
                    for err in ["error", "exception", "warning", "sql", "syntax"]
                ):
                    interesting_responses.append(
                        {"payload": payload, "reason": "error_pattern"}
                    )
                    print(f"[+] {param_name}={payload} → Error pattern detected")

                time.sleep(0.1)
            except Exception as e:
                print(f"[-] Error fuzzing {param_name}={payload}: {e}")
                continue

        if interesting_responses:
            param_info = {
                "param": param_name,
                "location": location,
                "interesting_responses": interesting_responses,
            }
            self.discovered_params.append(param_info)
            return param_info
        return None

    def fuzz_common_params(self) -> List[Dict]:
        print(f"[*] Fuzzing {len(self.common_params)} common parameters")
        results = []
        for param in self.common_params:
            result = self.fuzz_parameter(param)
            if result:
                results.append(result)
        return results

    def fuzz_custom_params(self, params: List[str]) -> List[Dict]:
        print(f"[*] Fuzzing {len(params)} custom parameters")
        results = []
        for param in params:
            result = self.fuzz_parameter(param)
            if result:
                results.append(result)
        return results

    def get_results(self) -> List[Dict]:
        return self.discovered_params

    def save_results(self, output_file: str = "recon/params.json") -> None:
        import os

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(self.discovered_params, f, indent=2)
        print(f"[*] Results saved to {output_file}")

    def close(self):
        self.session.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Parameter Fuzzer")
    parser.add_argument("target", help="Target URL")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    parser.add_argument("--threads", type=int, default=3, help="Max threads")
    parser.add_argument(
        "--output", "-o", default="recon/params.json", help="Output file"
    )
    parser.add_argument("--params-file", help="File with custom params to fuzz")
    args = parser.parse_args()

    fuzzer = ParameterFuzzer(
        target_url=args.target, timeout=args.timeout, max_threads=args.threads
    )
    fuzzer.get_baseline()

    if args.params_file:
        with open(args.params_file) as f:
            custom_params = [line.strip() for line in f if line.strip()]
        fuzzer.fuzz_custom_params(custom_params)
    else:
        fuzzer.fuzz_common_params()

    fuzzer.save_results(args.output)
    fuzzer.close()
    print(
        f"\n[*] Fuzzing complete. Found {len(fuzzer.get_results())} interesting parameters"
    )


if __name__ == "__main__":
    main()
