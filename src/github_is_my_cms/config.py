# src/github_is_my_cms/config.py
"""
Configuration loader for the README CMS.
Responsible for reading TOML files and instantiating the CMSConfig model.
"""

from __future__ import annotations

import logging
import sys
import tomllib
from pathlib import Path
from typing import Any, Dict

from httpie.output.ui.rich_help import to_help_message

from .models import CMSConfig

logger = logging.getLogger(__name__)

from collections import Counter


def assign_groups(
    projects_data: dict, top_n: int = 50, default_group: str = "other"
) -> dict:
    projects = projects_data

    languages = [
        project.get("primary_langauge").lower()
        for project in projects
        if project.get("primary_langauge")
    ]
    print(languages)
    # 1) Global tag frequency
    tag_counts = Counter()
    for p in projects:
        for t in p.get("tags") or []:
            if isinstance(t, str) and t.strip() and t.lower() not in languages:
                tag_counts[t.strip()] += 1

    # 2) Top-N tags with deterministic tie-break
    top_tags_sorted = sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    top_tags = [t for t, _ in top_tags_sorted[:top_n]]
    top_tag_set = set(top_tags)

    # Precompute ranking for fast "best tag" selection per project
    # Lower rank value = better
    top_tag_rank = {
        t: i for i, t in enumerate(top_tags)
    }  # already sorted by (-count, tag)

    # 3) Assign groups
    for p in projects:
        if p.get("group"):
            continue

        tags = [
            t.strip() for t in (p.get("tags") or []) if isinstance(t, str) and t.strip()
        ]
        candidate_tags = [
            t for t in tags if t in top_tag_set and t.lower() not in languages
        ]

        if candidate_tags:
            # Pick the best candidate by global rank (freq desc, then lex)
            best = min(candidate_tags, key=lambda t: top_tag_rank[t])
            p["group"] = best.title()
        elif p.get("primary_language"):
            p["group"] = p["primary_language"].title()
        else:
            p["group"] = default_group.title()

    # Optional: stash top tags for debugging/visibility
    # projects_data["_top_tags"] = top_tags
    # projects_data["_tag_counts"] = dict(tag_counts)

    return projects_data


class ConfigLoader:
    """
    Loads and merges data from multiple TOML sources as defined in GHIP-001.
    """

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        # CHANGED: Data directory is now expected in the user's project root, not the package source
        self.data_dir = self.root_dir / "data"
        self.config_file = self.root_dir / "readme_cms.toml"

    def _load_toml_file(self, filepath: Path) -> Dict[str, Any]:
        """Helper to safely load a TOML file if it exists."""
        if not filepath.exists():
            logger.warning(f"Config file at {filepath} not found")
            return {}
        with open(filepath, "rb") as f:
            logger.debug(f"Loading config from {filepath}")
            return tomllib.load(f)

    def load(self) -> CMSConfig:
        """
        Aggregates all data sources into a single validated CMSConfig object.
        """
        # 1. Load Main Config (readme_cms.toml)
        # Contains: modes, languages
        main_config = self._load_toml_file(self.config_file)

        # 2. Load Identity Data (identity.toml & identity_graph.toml)
        # GHIP separates these, but our Identity model aggregates them.
        identity_data = self._load_toml_file(self.data_dir / "identity.toml")
        graph_data = self._load_toml_file(self.data_dir / "identity_graph.toml")

        # --- NEW LOGIC START ---
        # 2a. Load Skills (Try skills.toml, fallback to identity.toml)
        skills_file = self.data_dir / "skills.toml"
        if skills_file.exists():
            logger.info("Loading skills from separated skills.toml")
            skills_data = self._load_toml_file(skills_file)
            # The file format is { skills = [ {category=..., skills=[...]} ] }
            # The Identity Model expects 'skills' to be that list.
            identity_data["skills"] = skills_data.get("skills", [])
        else:
            logger.info("Loading skills from identity.toml (legacy)")
            # Existing behavior: identity_data already contains 'skills' key
            pass

        # Merge identity graph into the main identity dict under 'profiles'
        # Expectation: identity.toml has basic info (name, tagline),
        # identity_graph.toml has specific social nodes.
        if "identities" in graph_data:
            # The model expects 'profiles', the file might name it 'identities'
            # per the example in the GHIP "Identity Graph" section.
            identity_data["profiles"] = graph_data["identities"]

        # 3. Load Projects (projects.toml)
        # Manually curated projects
        projects_data = self._load_toml_file(self.data_dir / "projects.toml")
        projects_list = projects_data.get("projects", [])
        assign_groups(projects_list)

        # 4. Load PyPI Metadata (pypi_projects.toml)
        # Automated data from weekly workflow
        pypi_data = self._load_toml_file(self.data_dir / "pypi_projects.toml")
        pypi_list = pypi_data.get("packages", [])

        # 4b. Load Work Experience
        experience_data = self._load_toml_file(self.data_dir / "work_experience.toml")
        experience_list = experience_data.get("experience", [])

        # 4c. Load Resume Artifacts
        resumes_data = self._load_toml_file(self.data_dir / "resumes.toml")
        resumes_list = resumes_data.get("resumes", [])

        # Optional compatibility: if resumes.toml missing, fall back to identity.resumes
        # (Identity.resumes is legacy; ResumeArtifact is the v2 path.)
        if not resumes_list and identity_data.get("resumes"):
            legacy = identity_data.get("resumes", [])
            resumes_list = [
                {
                    "id": f"legacy-{i}",
                    "label": r.get("label"),
                    "url": r.get("url"),
                    "description": r.get("description"),
                    "icon": r.get("icon", "📄"),
                    "format": "other",
                    "status": "active",
                }
                for i, r in enumerate(legacy)
                if r.get("label") and r.get("url")
            ]

        # 5. Assemble the final dictionary for Pydantic validation
        # We merge all top-level keys.
        config_dict = {
            "identity": identity_data,
            "modes": main_config.get("mode", {}),  # GHIP uses [mode] table
            "languages": main_config.get("languages", {}),
            "projects": projects_list,
            "pypi_packages": pypi_list,
            "theme": main_config.get("theme", "default"),
            "work_experience": experience_list,
            "resumes": resumes_list,
        }

        # 6. Validate and Return
        # This triggers all Pydantic validators, including "No Twitter/X".
        return CMSConfig(**config_dict)


def load_config(root_path: str = ".") -> CMSConfig:
    """Convenience entry point."""
    return ConfigLoader(Path(root_path)).load()
