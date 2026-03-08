import requests
import urllib3
from typing import List, Dict, Optional
from urllib.parse import urljoin
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class EndpointScanner:
    COMMON_PATHS = [
        "/admin",
        "/administrator",
        "/admin.php",
        "/admin/",
        "/wp-admin",
        "/phpmyadmin",
        "/api",
        "/api/v1",
        "/api/v2",
        "/graphql",
        "/rest",
        "/swagger",
        "/api-docs",
        "/openapi.json",
        "/login",
        "/signin",
        "/auth",
        "/authenticate",
        "/register",
        "/signup",
        "/logout",
        "/password",
        "/reset",
        "/debug",
        "/test",
        "/dev",
        "/staging",
        "/.git",
        "/.env",
        "/config",
        "/console",
        "/upload",
        "/download",
        "/files",
        "/media",
        "/assets",
        "/dashboard",
        "/profile",
        "/settings",
        "/account",
        "/users",
        "/user",
        "/status",
        "/health",
        "/version",
        "/info",
        "/metrics",
        "/backup",
        "/backups",
        "/logs",
        "/log",
        "/robots.txt",
        "/sitemap.xml",
        "/.well-known/security.txt",
        "/crossdomain.xml",
    ]

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        max_threads: int = 5,
        verify_ssl: bool = False,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_threads = max_threads
        self.verify_ssl = verify_ssl
        self.discovered_endpoints = []
        self.common_paths = self.COMMON_PATHS.copy()
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (RedTeam Scanner/1.0)"})

    def scan_path(self, path: str) -> Optional[Dict]:
        url = urljoin(self.base_url, path)
        try:
            response = self.session.get(
                url, timeout=self.timeout, verify=self.verify_ssl, allow_redirects=False
            )
            if 200 <= response.status_code < 400:
                endpoint_info = {
                    "url": url,
                    "path": path,
                    "status_code": response.status_code,
                    "method": "GET",
                    "content_length": len(response.content),
                    "content_type": response.headers.get("Content-Type", ""),
                    "server": response.headers.get("Server", ""),
                    "auth_required": response.status_code == 401,
                    "redirects_to": response.headers.get("Location", ""),
                    "parameters": [],
                }
                print(f"[+] Found: {url} (Status: {response.status_code})")
                return endpoint_info
        except requests.exceptions.Timeout:
            print(f"[-] Timeout: {url}")
        except requests.exceptions.ConnectionError:
            print(f"[-] Connection error: {url}")
        except Exception as e:
            print(f"[-] Error scanning {url}: {e}")
        return None

    def scan_common_paths(self) -> List[Dict]:
        print(f"[*] Scanning {len(self.common_paths)} common paths on {self.base_url}")
        discovered = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_path = {
                executor.submit(self.scan_path, path): path
                for path in self.common_paths
            }
            for future in as_completed(future_to_path):
                result = future.result()
                if result:
                    discovered.append(result)
        self.discovered_endpoints.extend(discovered)
        print(f"[*] Discovered {len(discovered)} endpoints")
        return discovered

    def scan_custom_paths(self, paths: List[str]) -> List[Dict]:
        print(f"[*] Scanning {len(paths)} custom paths")
        discovered = []
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_path = {
                executor.submit(self.scan_path, path): path for path in paths
            }
            for future in as_completed(future_to_path):
                result = future.result()
                if result:
                    discovered.append(result)
        self.discovered_endpoints.extend(discovered)
        return discovered

    def get_results(self) -> List[Dict]:
        return self.discovered_endpoints

    def save_results(self, output_file: str = "recon/endpoints.json") -> None:
        import os

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(self.discovered_endpoints, f, indent=2)
        print(f"[*] Results saved to {output_file}")

    def close(self):
        self.session.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Endpoint Scanner")
    parser.add_argument("target", help="Target base URL")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout")
    parser.add_argument("--threads", type=int, default=5, help="Max threads")
    parser.add_argument(
        "--output", "-o", default="recon/endpoints.json", help="Output file"
    )
    parser.add_argument("--paths-file", help="File with custom paths to scan")
    args = parser.parse_args()

    scanner = EndpointScanner(
        base_url=args.target, timeout=args.timeout, max_threads=args.threads
    )
    scanner.scan_common_paths()

    if args.paths_file:
        with open(args.paths_file) as f:
            custom_paths = [line.strip() for line in f if line.strip()]
        scanner.scan_custom_paths(custom_paths)

    scanner.save_results(args.output)
    scanner.close()
    print(f"\n[*] Scan complete. Found {len(scanner.get_results())} endpoints")


if __name__ == "__main__":
    main()
