from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from github_is_my_cms.data_sources import (
    GitHubFetcher,
    PyPIDiscoveryFetcher,
    PyPIStatsFetcher,
)


class FakeResponse:
    def __init__(self, payload: Dict[str, Any], status: int = 200):
        self._payload = payload
        self.status = status

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def test_github_fetcher_uses_cache(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    fetcher = GitHubFetcher(cache_dir)
    payload = [{"name": "repo-one"}]

    fetcher.cache_file.write_text(json.dumps(payload), encoding="utf-8")

    assert fetcher.fetch_repos() == payload


def test_pypi_discovery_fetcher_uses_cache(tmp_path: Path) -> None:
    cache_dir = tmp_path / "cache"
    fetcher = PyPIDiscoveryFetcher(cache_dir)
    payload = {"user": "tester", "packages": ["alpha", "bravo"]}

    fetcher.cache_file.write_text(json.dumps(payload), encoding="utf-8")

    assert fetcher.fetch_user_packages("tester") == ["alpha", "bravo"]


def test_pypi_stats_fetcher_parses_keywords_and_repo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fetcher = PyPIStatsFetcher()
    payload = {
        "info": {
            "version": "1.2.3",
            "summary": "Demo package",
            "home_page": "https://example.com",
            "project_urls": {"Source": "https://github.com/example/demo"},
            "keywords": "tag1, tag2",
        }
    }

    def fake_urlopen(request: Any) -> FakeResponse:
        return FakeResponse(payload)

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    details = fetcher.fetch_details("demo")

    assert details["github_repo"] == "example/demo"
    assert details["tags"] == ["tag1", "tag2"]
