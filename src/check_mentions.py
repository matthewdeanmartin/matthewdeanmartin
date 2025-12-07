#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Iterable, List, Set


GH_USER: str = "matthewdeanmartin"
README_PATH: Path = Path("README.md")


def run_gh_command(args: Iterable[str]) -> str:
    """Run `gh` command and return stdout. Raises on error."""
    cmd: List[str] = ["gh", *args]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"`{' '.join(cmd)}` failed with exit {result.returncode}: {result.stderr}"
        )
    return result.stdout


def get_all_public_non_archived_non_fork_repos(user: str) -> Set[str]:
    """
    List all repos for the user that are:
        - public
        - NOT archived
        - NOT forks
    """
    stdout: str = run_gh_command(
        [
            "repo",
            "list",
            user,
            "--limit",
            "1000",
            "--json",
            "name,isPrivate,isArchived,isFork",
        ]
    )

    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from gh: {exc}") from exc

    repos: Set[str] = set()
    for repo in data:
        name = repo.get("name")
        if not name:
            continue
        private = bool(repo.get("isPrivate"))
        archived = bool(repo.get("isArchived"))
        fork = bool(repo.get("isFork"))
        if private or archived or fork:
            continue
        repos.add(name)

    return repos


def extract_repo_names_from_readme(user: str, readme_path: Path) -> Set[str]:
    """Extract repo names linked in README pointing to the given user."""
    if not readme_path.exists():
        raise FileNotFoundError(f"Missing README.md at: {readme_path}")

    text: str = readme_path.read_text(encoding="utf-8", errors="ignore")

    # Detect URLs like https://github.com/user/repo or .../repo.git
    pattern = re.compile(
        rf"https?://github\.com/{re.escape(user)}/([A-Za-z0-9_.\-]+)",
        re.IGNORECASE,
    )

    repos: Set[str] = set()
    for match in pattern.finditer(text):
        repo = match.group(1)
        if repo.endswith(".git"):
            repo = repo[:-4]
        repos.add(repo)

    return repos


def main() -> None:
    all_repos: Set[str] = get_all_public_non_archived_non_fork_repos(GH_USER)
    readme_repos: Set[str] = extract_repo_names_from_readme(GH_USER, README_PATH)
    missing: Set[str] = all_repos - readme_repos

    print(f"User: {GH_USER}")
    print()
    print(f"Public, non-archived, non-fork repos: {len(all_repos)}")
    print(f"Repos referenced in README:           {len(readme_repos)}")
    print(f"Missing from README:                  {len(missing)}")
    print()

    if not missing:
        print("README.md references all eligible repositories.")
    else:
        print("Repos NOT referenced in README.md:")
        for r in sorted(missing):
            print(f"- {r}")


if __name__ == "__main__":
    main()
