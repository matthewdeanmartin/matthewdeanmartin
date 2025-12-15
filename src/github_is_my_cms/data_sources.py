"""
data_sources.py
Handles fetching external data from PyPI and GitHub APIs to update local TOML caches.
"""

import json
import logging
from typing import List
from pathlib import Path
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

import json
import logging
import shutil
import subprocess
import tomllib
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import tomli_w

from .config import load_config  # Needed to get the username

logger = logging.getLogger(__name__)



class BaseFetcher:
    """Base class for cached fetchers."""

    def __init__(self, cache_dir: Path, cache_filename: str):
        self.cache_dir = cache_dir
        self.cache_file = self.cache_dir / cache_filename
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _is_cache_valid(self) -> bool:
        """Returns True if cache exists and is less than 24 hours old."""
        if not self.cache_file.exists():
            return False
        mtime = self.cache_file.stat().st_mtime
        age = datetime.now().timestamp() - mtime
        return age < (24 * 60 * 60)  # 24 hours


class GitHubFetcher(BaseFetcher):
    """
    Fetches repository metadata using the 'gh' CLI tool.
    Implements a 24-hour file-based cache.
    """

    def __init__(self, cache_dir: Path):
        super().__init__(cache_dir, "github_repos.json")

    def fetch_repos(self) -> List[Dict[str, Any]]:
        """
        Returns a list of public repositories.
        Uses cached data if fresh; otherwise calls 'gh repo list'.
        """
        # 1. Check Cache
        if self._is_cache_valid():
            logger.info("GitHub: Using cached repository data.")
            try:
                return json.loads(self.cache_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                logger.warning("GitHub: Cache corrupted. Refetching.")

        # 2. Fetch via GH CLI
        if not shutil.which("gh"):
            logger.error("GitHub: 'gh' CLI not found on PATH. Cannot sync projects.")
            return []

        logger.info("GitHub: Fetching fresh repository list...")

        # Fields to fetch: name, description, url, isArchived, repositoryTopics, homepageUrl
        cmd = [
            "gh",
            "repo",
            "list",
            "--public",  # Exclude private repos
            "--source",  # Exclude forks (optional, usually preferred for profiles)
            "--limit",
            "1000",  # Ensure we get everything
            "--json",
            "name,description,url,isArchived,repositoryTopics,homepageUrl",
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)

            # 3. Update Cache
            self.cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return data

        except subprocess.CalledProcessError as e:
            logger.error(f"GitHub: CLI command failed: {e.stderr}")
            return []
        except json.JSONDecodeError:
            logger.error("GitHub: Failed to parse CLI output.")
            return []




logger = logging.getLogger(__name__)


class PyPIDiscoveryFetcher(BaseFetcher):
    """
    Finds all packages owned by a specific PyPI user by scraping their profile page.
    """

    BASE_URL = 'https://pypi.org/user'

    def __init__(self, cache_dir: Path):
        super().__init__(cache_dir, "pypi_discovery.json")

    def fetch_user_packages(self, username: str) -> List[str]:
        """
        Returns a list of package names owned by the user.
        """
        if not username:
            return []

        # 1. Check Cache
        if self._is_cache_valid():
            try:
                data = json.loads(self.cache_file.read_text(encoding="utf-8"))
                if data.get("user") == username:
                    logger.info(f"PyPI: Using cached package list for user '{username}'.")
                    return data.get("packages", [])
            except json.JSONDecodeError:
                pass

        # 2. Fetch via HTTPX + BS4
        logger.info(f"PyPI: Discovering packages for user '{username}' via HTML scraping...")

        target_url = f"{self.BASE_URL}/{username}/"
        package_names = []

        try:
            # It is good practice to include a User-Agent
            headers = {"User-Agent": "PyPIDiscoveryFetcher/1.0"}

            with httpx.Client(timeout=10.0) as client:
                response = client.get(target_url, headers=headers)

                if response.status_code == 404:
                    logger.warning(f"PyPI: User '{username}' not found.")
                    return []

                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # PyPI user pages list packages using the class 'package-snippet__title'
                snippets = soup.select(".package-snippet__title")
                package_names = sorted(list(set(s.get_text(strip=True) for s in snippets)))

            # 3. Save Cache
            cache_payload = {
                "user": username,
                "timestamp": datetime.now().isoformat(),
                "packages": package_names
            }
            self.cache_file.write_text(json.dumps(cache_payload, indent=2), encoding="utf-8")

            return package_names

        except httpx.HTTPError as e:
            logger.error(f"PyPI Discovery HTTP error: {e}")
            return []
        except Exception as e:
            logger.error(f"PyPI Discovery failed: {e}")
            return []


class PyPIStatsFetcher:
    """
    Fetches detailed metadata for a specific package from JSON API.
    Does not cache individual files to avoid thousands of small files;
    relies on upper layer to manage frequency or the global build cache.
    """
    BASE_URL = "https://pypi.org/pypi/{package}/json"

    def fetch_details(self, package_name: str) -> Dict[str, Any]:
        url = self.BASE_URL.format(package=package_name)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'github-is-my-cms/0.1.0'})
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    return {}
                data = json.loads(response.read().decode())
                info = data.get("info", {})

                return {
                    "package_name": package_name,
                    "version": info.get("version"),
                    "summary": info.get("summary"),
                    "docs_url": info.get("home_page") or info.get("project_url"),
                    # Note: pypistats.org is required for real download counts.
                    # Providing a placeholder or existing logic here.
                    "last_updated": date.today().isoformat(),
                    # Attempt to find GitHub repo in project_urls
                    "github_repo": self._extract_github_repo(info.get("project_urls") or {})
                }
        except urllib.error.URLError as e:
            logger.warning(f"Failed to fetch details for {package_name}: {e}")
            return {}

    def _extract_github_repo(self, urls: Dict[str, str]) -> Optional[str]:
        """Tries to find 'owner/repo' from project links."""
        for url in urls.values():
            if url and "github.com" in url:
                # Naive parse: https://github.com/owner/repo
                parts = [p for p in url.split("/") if p]
                if "github.com" in parts:
                    idx = parts.index("github.com")
                    if idx + 2 < len(parts):
                        return f"{parts[idx + 1]}/{parts[idx + 2]}"
        return ""

class PyPIFetcher:
    """
    Fetches metadata from PyPI JSON API.
    """

    BASE_URL = "https://pypi.org/pypi/{package}/json"

    def fetch(self, package_name: str) -> Dict[str, Any]:
        url = self.BASE_URL.format(package=package_name)
        try:
            with urllib.request.urlopen(url) as response:
                if response.status != 200:
                    logger.warning(
                        f"PyPI: {package_name} returned status {response.status}"
                    )
                    return {}
                data = json.loads(response.read().decode())

                info = data.get("info", {})

                # Extract relevant fields
                return {
                    "package_name": package_name,
                    "version": info.get("version"),
                    "summary": info.get("summary"),
                    "docs_url": info.get("home_page") or info.get("project_url"),
                    # Note: PyPI JSON no longer provides download stats directly.
                    # We retain existing counts or set to 0.
                    # Real impl requires pypistats.org API.
                    "last_updated": date.today().isoformat(),
                }
        except urllib.error.URLError as e:
            logger.error(f"Failed to fetch PyPI data for {package_name}: {e}")
            return {}


class DataUpdater:
    """
    Orchestrates the update of local TOML files with remote data.
    """

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.data_dir = self.root_dir / "data"
        self.cache_dir = self.root_dir / ".cache"

        self.projects_file = self.data_dir / "projects.toml"
        self.pypi_file = self.data_dir / "pypi_projects.toml"
        # Cache location (hidden inside data or a temp dir)
        self.cache_dir = self.root_dir / ".cache"

        # Initialize Fetchers
        self.gh_fetcher = GitHubFetcher(self.cache_dir)
        self.pypi_discovery = PyPIDiscoveryFetcher(self.cache_dir)
        self.pypi_details = PyPIStatsFetcher()

        # Load config to get usernames
        # Note: We do this here so the CLI doesn't have to pass the config obj
        try:
            self.config = load_config(str(self.root_dir))
        except Exception:
            logger.warning("Could not load full config; some auto-discovery features may fail.")
            self.config = None

    def _load_toml(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, "rb") as f:
            return tomllib.load(f)

    def update_projects_from_github(self):
        """
        Syncs projects.toml with GitHub.
        Preserves 'cms' directives and unknown non-GitHub projects.
        """
        logger.info("Syncing projects from GitHub...")

        # Check if we should filter by specific user (if configured)
        target_user = self.config.identity.github_username if self.config else None

        # 1. Load Existing Data
        existing_data = self._load_toml(self.projects_file)
        existing_projects = existing_data.get("projects", [])

        # Create a lookup for existing projects by slug
        # We assume slug == repo name for GitHub projects
        project_map = {p["slug"]: p for p in existing_projects}

        # 2. Fetch Fresh Data
        gh_repos = self.gh_fetcher.fetch_repos()
        if not gh_repos:
            logger.warning("No repositories found or fetch failed.")
            return

        active_slugs = set()

        for repo in gh_repos:
            # If a target user is set in config, strict filter, otherwise accept all found by 'gh'
            # (assuming 'gh' is authenticated as the user)
            # repo_owner = repo['name'].split('/')[0] if '/' in repo['name'] else ''
            # Note: gh repo list usually returns 'owner/repo' in name field?
            # Actually, standard json output name is just 'repo'. owner is separate.
            # Let's trust the current 'gh repo list' context.

            slug = repo["name"]
            active_slugs.add(slug)

            # Extract GitHub Data
            description = repo.get("description") or ""
            url = repo.get("url")
            homepage = repo.get("homepageUrl")
            topics = [t["name"] for t in (repo.get("repositoryTopics", []) or [])]
            is_archived = repo.get("isArchived", False)

            status = "archived" if is_archived else "active"

            # 3. Merge Strategy
            if slug in project_map:
                # Update existing entry
                entry = project_map[slug]

                # Overwrite synced fields
                entry["description"] = description
                entry["repository_url"] = url
                # If homepage is set on GH, use it as 'url' (project link),
                # otherwise fallback to repo url or keep existing.
                if homepage:
                    entry["url"] = homepage
                elif "url" not in entry:
                    entry["url"] = url

                entry["tags"] = topics
                entry["status"] = status

                # CMS Directive Preservation:
                # We simply DON'T touch the 'cms' key if it exists.
                # If the user wants to add one, they do it manually in the TOML.
            else:
                # Create new entry
                entry = {
                    "slug": slug,
                    "name": slug,  # Default name to slug
                    "description": description,
                    "url": homepage if homepage else url,
                    "repository_url": url,
                    "tags": topics,
                    "status": status,
                    # Initialize empty CMS directive container for future use
                    "cms": {"suppress": False, "package_links": []},
                }
                project_map[slug] = entry

            # Mark missing as gone
            for slug, entry in project_map.items():
                if slug not in active_slugs:
                    if "github.com" in str(entry.get("repository_url", "")):
                        entry["status"] = "gone"

            sorted_projects = sorted(project_map.values(), key=lambda x: x["slug"])
            with open(self.projects_file, "wb") as f:
                tomli_w.dump({"projects": sorted_projects}, f)

            logger.info(f"Synced {len(sorted_projects)} projects.")

    def update_pypi_data(self):
        """
        Discovers packages via PyPI XML-RPC (if username configured)
        and updates metadata for all packages.
        """
        # 1. Load Existing Data
        if self.pypi_file.exists():
            with open(self.pypi_file, "rb") as f:
                data = tomllib.load(f)
            existing_packages = data.get("packages", [])
        else:
            existing_packages = []

        # Map: package_name -> dict
        pkg_map = {p["package_name"]: p for p in existing_packages if "package_name" in p}

        # 2. Discovery Phase
        pypi_user = self.config.identity.pypi_username if self.config else None

        if pypi_user:
            logger.info(f"Discovering packages for PyPI user: {pypi_user}")
            discovered_names = self.pypi_discovery.fetch_user_packages(pypi_user)

            for name in discovered_names:
                if name not in pkg_map:
                    # Initialize new entry
                    pkg_map[name] = {
                        "package_name": name,
                        "downloads_monthly": 0,  # Placeholder
                    }
        else:
            logger.info("No pypi_username configured in identity.toml. Skipping auto-discovery.")

        # 3. Detail Update Phase
        updated_list = []
        logger.info(f"Updating details for {len(pkg_map)} packages...")

        for name, pkg_data in pkg_map.items():
            logger.debug(f"Fetching details for {name}...")
            details = self.pypi_details.fetch_details(name)
            if details:
                # Merge logic: Remote details overwrite cached details,
                # but manual overrides in TOML (if any existed and we cared)
                # usually require logic. Here we assume PyPI is truth for metadata.

                # Preserve existing fields that PyPI fetcher doesn't return (like manual downloads override)
                downloads = pkg_data.get("downloads_monthly", 0)

                pkg_data.update(details)

                # Restore/Keep downloads if not fetched (fetching downloads requires bigquery/pypistats)
                pkg_data["downloads_monthly"] = downloads

            updated_list.append(pkg_data)

        # 4. Sort and Save
        updated_list.sort(key=lambda x: x["package_name"].lower())

        with open(self.pypi_file, "wb") as f:
            tomli_w.dump({"packages": updated_list}, f)

        logger.info(f"Successfully updated {self.pypi_file} with {len(updated_list)} packages.")