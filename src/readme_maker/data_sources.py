"""
data_sources.py
Handles fetching external data from PyPI and GitHub APIs to update local TOML caches.
"""
import json
import logging
import urllib.request
import urllib.error
import subprocess
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import List, Dict, Any
import tomli_w
import tomllib




logger = logging.getLogger(__name__)

class GitHubFetcher:
    """
    Fetches repository metadata using the 'gh' CLI tool.
    Implements a 24-hour file-based cache.
    """

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_file = self.cache_dir / "github_repos.json"

        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _is_cache_valid(self) -> bool:
        """Returns True if cache exists and is less than 24 hours old."""
        if not self.cache_file.exists():
            return False

        mtime = self.cache_file.stat().st_mtime
        age = datetime.now().timestamp() - mtime
        return age < (24 * 60 * 60)  # 24 hours in seconds

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

        # Fields to fetch: name, description, url, isArchived, repositoryTopics
        cmd = [
            "gh", "repo", "list",
            "--public",  # Exclude private repos
            "--source",  # Exclude forks (optional, usually preferred for profiles)
            "--limit", "1000",  # Ensure we get everything
            "--json", "name,description,url,isArchived,repositoryTopics,homepageUrl"
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
                    logger.warning(f"PyPI: {package_name} returned status {response.status}")
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
                    "last_updated": date.today().isoformat()
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
        self.projects_file = self.data_dir / "projects.toml"
        self.pypi_file = self.data_dir / "pypi_projects.toml"
        # Cache location (hidden inside data or a temp dir)
        self.cache_dir = self.root_dir / ".cache"

        self.gh_fetcher = GitHubFetcher(self.cache_dir)
        self.fetcher = PyPIFetcher()

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
            slug = repo["name"]
            active_slugs.add(slug)

            # Extract GitHub Data
            description = repo.get("description") or ""
            url = repo.get("url")
            homepage = repo.get("homepageUrl")
            topics = [t["name"] for t in repo.get("repositoryTopics", [])]
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
                    "cms": {
                        "suppress": False,
                        "package_links": []
                    }
                }
                project_map[slug] = entry

        # 4. Handle "Gone" Projects
        # If a project was in TOML, has a github.com repo_url, but was NOT returned by GH,
        # it is likely private or deleted.
        for slug, entry in project_map.items():
            if slug not in active_slugs:
                repo_url = str(entry.get("repository_url", ""))
                if "github.com" in repo_url:
                    # It was a github repo, but now it's gone from the public list
                    logger.info(f"Project {slug} not found in public GitHub list. Marking as 'gone'.")
                    entry["status"] = "gone"
                else:
                    # It's a manual project (not hosted on GH), leave it alone.
                    pass

        # 5. Write back to TOML
        # Reconstruct list from map (sorted by name for stability)
        sorted_projects = sorted(project_map.values(), key=lambda x: x["slug"])
        output_data = {"projects": sorted_projects}

        if HAS_TOML_WRITER:
            with open(self.projects_file, "wb") as f:
                tomli_w.dump(output_data, f)
            logger.info(f"Successfully synced {len(sorted_projects)} projects to {self.projects_file}")
        else:
            logger.error("Cannot write TOML: 'tomli-w' missing.")


    def update_pypi_data(self):
        """
        Reads pypi_projects.toml, fetches updates for all listed packages, and rewrites the file.
        """
        if not self.pypi_file.exists():
            logger.warning(f"No pypi_projects.toml found at {self.pypi_file}")
            return

        # 1. Read existing data to get the list of packages to track
        # We use simple read to preserve the list structure if possible,
        # but here we rely on the ConfigLoader logic or just standard toml loading.
        # For the updater, we need the raw dict.
        import sys
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib

        with open(self.pypi_file, "rb") as f:
            data = tomllib.load(f)

        current_packages = data.get("packages", [])
        if not current_packages:
            logger.info("No packages found in pypi_projects.toml")
            return

        updated_packages = []
        logger.info(f"Updating metadata for {len(current_packages)} PyPI packages...")

        for pkg in current_packages:
            name = pkg.get("package_name")
            if not name:
                continue

            logger.info(f"Fetching: {name}...")
            remote_data = self.fetcher.fetch(name)

            if remote_data:
                # Merge remote data into existing (preserving manual overrides like github_repo if not fetched)
                # We prioritize remote version/summary/updated, but keep manual config like github_repo
                pkg.update(remote_data)

            updated_packages.append(pkg)

        # 2. Write back to TOML
        output_data = {"packages": updated_packages}

        if HAS_TOML_WRITER:
            with open(self.pypi_file, "wb") as f:
                tomli_w.dump(output_data, f)
            logger.info(f"Successfully updated {self.pypi_file}")
        else:
            logger.error("Cannot write TOML: 'tomli-w' package is missing. Install it via pip.")
            # Fallback: Print what we would have written
            logger.debug(json.dumps(output_data, indent=2))