# src/github_is_my_cms/builder.py
"""
The core build engine for the README CMS.
Compiles Jinja templates + TOML data + Markdown content into final artifacts.
"""

import datetime
import logging
import math
import re
import shutil
from collections import defaultdict
from pathlib import Path

import orjson
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import HttpUrl

from .config import load_config
from .models import CMSConfig

logger = logging.getLogger(__name__)


class SiteBuilder:
    """
    Orchestrates the generation of Markdown, HTML, and Static API files.
    """

    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.projects_by_skill = {}
        self.config: CMSConfig = load_config(str(self.root))

        # TODO: this is messed up. It should be from editable installation or package.
        self.src = self.root / "src"
        self.content_dir = self.src / "content"
        self.templates_dir = (
            self.src / "github_is_my_cms" / "templates" / self.config.theme
        )
        self.docs_dir = self.root / "docs"
        self.md_out = self.docs_dir / "md"
        self.api_out = self.docs_dir / "apis"
        self.html_out = self.docs_dir

        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # --- PRE-PROCESSING LOGIC ---

        # 1. APPLY FEATURED LOGIC (NEW)
        self._apply_featured_status()

        # 2. Filter based on "Hide Archived" config
        raw_projects = self.config.projects
        should_hide_archived = getattr(
            self.config.current_mode_settings, "hide_archived", False
        )

        if should_hide_archived:
            logger.info("Mode setting 'hide_archived' is ON. Filtering list.")
            visible_projects = [p for p in raw_projects if p.status != "archived"]
        else:
            visible_projects = raw_projects

        # 3. Sort projects (Featured first, then Alphabetical)
        visible_projects.sort(key=lambda x: (not x.featured, x.name.lower()))

        # 4. Extract Featured Projects
        featured_projects = [p for p in visible_projects if p.featured]

        # 5. Create Groups
        projects_by_group = defaultdict(list)
        for p in visible_projects:
            g = p.group if p.group else "Other"
            projects_by_group[g].append(p)

        # Inject Globals
        self.env.globals["projects"] = visible_projects
        self.env.globals["featured_projects"] = featured_projects
        self.env.globals["projects_by_group"] = dict(projects_by_group)
        self.env.globals["generation"] = {"generated_at": datetime.datetime.now()}
        self.env.globals["config"] = self.config
        self.env.globals["identity"] = self.config.identity
        self.env.globals["mode"] = self.config.current_mode_settings
        self.env.globals["pypi"] = self.config.pypi_packages
        self.env.globals["work_experience"] = self.config.work_experience
        self.env.globals["resumes"] = self.config.resumes
        self.env.globals["include_content"] = self._read_content_file

    def _slugify(self, text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

    # --- NEW HELPER METHODS ---

    def _normalize_name_match(self, name: str) -> str:
        """
        Normalizes a project name for comparison.
        Case insensitive, treats '-' and '_' as identical.
        Example: "Bash2Gitlab" -> "bash2gitlab", "naive_linkbacks" -> "naivelinkbacks"
        """
        if not name:
            return ""
        # Remove both - and _ to make them strictly equivalent
        return re.sub(r"[-_]", "", name.lower())

    def _apply_featured_status(self):
        """
        Updates the .featured boolean on all Projects and PyPI packages
        based on the list defined in identity.toml for the CURRENT mode.
        """
        mode = self.config.modes.current
        identity = self.config.identity

        # Determine which list of strings to use
        target_list = []
        if mode == "job_hunting":
            target_list = identity.job_hunting_projects
        elif mode == "project_promotion":
            target_list = identity.project_promotion
        elif mode == "self_promotion":
            # If self_promotion logic isn't strictly defined, fallback or use identity_projects
            target_list = identity.identity_projects
        else:
            # Fallback
            target_list = identity.project_promotion

        # Create a set of normalized names for O(1) lookup
        featured_slugs = {self._normalize_name_match(name) for name in target_list}

        logger.info(
            f"Applying featured status for mode '{mode}'. {len(featured_slugs)} targets found."
        )

        # Apply to GitHub Projects
        for proj in self.config.projects:
            norm_name = self._normalize_name_match(proj.name)
            if norm_name in featured_slugs:
                proj.featured = True
            else:
                # IMPORTANT: Reset to False if not in the list, so mode switches work cleanly
                proj.featured = False

        # Apply to PyPI Packages (if you want stars there too)
        # Note: PyPIPackage model doesn't explicitly have 'featured',
        # but Python allows setting dynamic attributes or you can add it to the model.
        for pkg in self.config.pypi_packages:
            norm_name = self._normalize_name_match(pkg.package_name)
            # Dynamically set attribute for template usage
            pkg.featured = norm_name in featured_slugs

    # ... existing methods (_map_relationships, build_skill_pages, etc) ...
