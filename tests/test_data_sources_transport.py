"""Exercise PyPI discovery with real local HTTP and the installed HTTPX2 API."""

from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

from github_is_my_cms.data_sources import PyPIDiscoveryFetcher


@pytest.fixture
def profile_server() -> Iterator[tuple[str, list[str]]]:
    requests: list[str] = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            requests.append(self.path)
            if "missing" in self.path:
                body = b"missing"
                self.send_response(404)
            else:
                body = ('<h3 class="package-snippet__title">zebra</h3><h3 class="package-snippet__title">alpha</h3><h3 class="package-snippet__title">alpha</h3>').encode()
                self.send_response(200)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format_string: str, *args: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/user", requests
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def test_discovery_preserves_sorted_unique_packages_and_cache(profile_server: tuple[str, list[str]], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    url, requests = profile_server
    monkeypatch.setattr(PyPIDiscoveryFetcher, "BASE_URL", url)
    monkeypatch.setenv("NO_PROXY", "127.0.0.1")
    fetcher = PyPIDiscoveryFetcher(tmp_path)
    assert fetcher.fetch_user_packages("example") == ["alpha", "zebra"]
    assert fetcher.fetch_user_packages("example") == ["alpha", "zebra"]
    assert len(requests) == 1


def test_discovery_handles_missing_profile(profile_server: tuple[str, list[str]], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    url, requests = profile_server
    monkeypatch.setattr(PyPIDiscoveryFetcher, "BASE_URL", url)
    monkeypatch.setenv("NO_PROXY", "127.0.0.1")
    assert PyPIDiscoveryFetcher(tmp_path).fetch_user_packages("missing") == []
    assert len(requests) == 1
