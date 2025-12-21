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

        # Load Configuration (Data Layer)
        self.config: CMSConfig = load_config(str(self.root))

        # TODO: this is messed up. It should be from editable installation or package.
        self.src = self.root / "src"
        self.content_dir = self.src / "content"
        self.templates_dir = (
            self.src / "github_is_my_cms" / "templates" / self.config.theme
        )

        # Output directories
        self.docs_dir = self.root / "docs"
        self.md_out = self.docs_dir / "md"
        self.api_out = self.docs_dir / "apis"
        self.html_out = self.docs_dir  # HTML sits in root of docs/ for GitHub Pages

        # Setup Jinja2 Environment
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # --- PRE-PROCESSING LOGIC ---

        # 1. Filter based on "Hide Archived" config
        raw_projects = self.config.projects
        should_hide_archived = getattr(
            self.config.current_mode_settings, "hide_archived", False
        )

        if should_hide_archived:
            logger.info("Mode setting 'hide_archived' is ON. Filtering list.")
            visible_projects = [p for p in raw_projects if p.status != "archived"]
        else:
            visible_projects = raw_projects

        # 2. Sort projects (Featured first, then Alphabetical)
        visible_projects.sort(key=lambda x: (not x.featured, x.name.lower()))

        # 3. Extract Featured Projects
        featured_projects = [p for p in visible_projects if p.featured]

        # 4. Create Groups
        # Structure: { "Group Name": [Project, Project], ... }
        projects_by_group = defaultdict(list)
        for p in visible_projects:
            # Fallback if group is missing in data (though model defaults to 'Other')
            g = p.group if p.group else "Other"
            projects_by_group[g].append(p)

        # Inject Globals and Helpers
        # Overwrite the raw list with the filtered list
        self.env.globals["projects"] = visible_projects

        # Add new convenience lists
        self.env.globals["featured_projects"] = featured_projects
        self.env.globals["projects_by_group"] = dict(
            projects_by_group
        )  # convert to standard dict

        self.env.globals["generation"] = {"generated_at": datetime.datetime.now()}

        self.env.globals["config"] = self.config
        self.env.globals["identity"] = self.config.identity
        self.env.globals["mode"] = self.config.current_mode_settings
        self.env.globals["pypi"] = self.config.pypi_packages

        self.env.globals["work_experience"] = self.config.work_experience
        self.env.globals["resumes"] = self.config.resumes

        # Helper to include raw markdown content from src/content/
        self.env.globals["include_content"] = self._read_content_file

    # Add this helper method
    def _slugify(self, text: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

    def _map_relationships(self):
        """
        Matches Skills to Projects using Name + Aliases.
        """
        logger.info("-> Mapping Data Relationships...")

        self.projects_by_skill = {}

        # 1. Create a "Lookup Map" for resume linking later
        # Maps "alias" -> "canonical_skill_slug"
        # e.g. {"psql": "postgres", "postgresql": "postgres"}
        self.skill_lookup_map = {}

        # Combine all searchable items
        all_content_items = self.config.projects + self.config.pypi_packages

        for group in self.config.identity.skills:
            for skill in group.skills:
                skill_slug = self._slugify(skill.name)
                skill.page_slug = skill_slug

                # 2. Build the Search Set for this skill
                # Normalize to lowercase for case-insensitive matching
                search_terms = {skill.name.lower()}
                if skill.aliases:
                    search_terms.update(t.lower() for t in skill.aliases)

                # Populate the lookup map for Work Experience linking
                for term in search_terms:
                    self.skill_lookup_map[term] = skill_slug

                matching_items = []

                for item in all_content_items:
                    # 3. Gather all "tags" from the item
                    item_tags = set()

                    # Add Explicit Tags
                    if hasattr(item, "tags") and item.tags:
                        item_tags.update(t.lower() for t in item.tags)

                    # Add Primary Language (for GitHub)
                    if hasattr(item, "primary_language") and item.primary_language:
                        item_tags.add(item.primary_language.lower())

                    # Add Implicit Python for PyPI
                    if hasattr(item, "package_name"):  # It's a PyPI package
                        item_tags.add("python")

                    # 4. INTERSECTION: Do any search terms exist in item tags?
                    if not search_terms.isdisjoint(item_tags):
                        matching_items.append(item)

                    # 5. Check Manual Overrides (related_skills)
                    if hasattr(item, "related_skills") and item.related_skills:
                        if skill.name in item.related_skills:
                            if item not in matching_items:
                                matching_items.append(item)

                if matching_items:
                    self.projects_by_skill[skill.name] = matching_items

        # Inject the lookup map into Jinja globals for use in templates
        self.env.globals["skill_lookup_map"] = self.skill_lookup_map

    def build_skill_pages(self):
        """Generates individual HTML pages for skills."""
        self._map_relationships()
        logger.info("-> Building Skill Detail Pages...")

        # Check if template exists
        template_name = "pages/skill_detail.html.j2"
        if not (self.templates_dir / template_name).exists():
            logger.warning(f"Template {template_name} not found, skipping skill pages.")
            raise Exception()

        template = self.env.get_template(template_name)

        # Output directory: docs/skills/
        skills_out = self.html_out / "skills"
        skills_out.mkdir(parents=True, exist_ok=True)

        if not self.projects_by_skill:
            logger.warning("No skills found")
        else:
            logger.info(f"Processing {len(self.projects_by_skill)}")

        for skill_name, specific_projects in self.projects_by_skill.items():
            print(skill_name, len(specific_projects))
            skill_slug = self._slugify(skill_name)

            # KEY FIX: passing 'skill_projects' (unique name), not 'projects'
            rendered = template.render(
                skill_name=skill_name, skill_projects=specific_projects
            )

            (skills_out / f"{skill_slug}.html").write_text(rendered, encoding="utf-8")

    def _read_content_file(self, filename: str) -> str:
        """
        Helper for Jinja templates to pull in raw content.
        Example usage in template: {{ include_content('pages/about.md') }}
        """
        file_path = self.content_dir / filename
        if not file_path.exists():
            return ""
        return file_path.read_text(encoding="utf-8")

    def clean(self):
        """
        Cleans output directories to ensure a fresh build.
        """
        logger.info(f"Cleaning paths: {[self.md_out, self.api_out]}")
        for path in [self.md_out, self.api_out]:
            if path.exists():
                shutil.rmtree(path)
            path.mkdir(parents=True, exist_ok=True)

    def build_markdown_pages(self):
        """
        Compiles templates/pages/*.md.j2 into docs/md/*.md
        """
        self._map_relationships()
        logger.info(
            f"-> Building Markdown Pages (Mode: {self.config.modes.current})..."
        )

        pages_dir = self.templates_dir / "pages"
        if not pages_dir.exists():
            logger.warning("Warning: No pages templates found.")
            return

        count = 0
        for template_path in pages_dir.glob("*.md.j2"):
            template_name = template_path.name
            target_name = template_name.replace(".j2", "")

            # Render template
            template = self.env.get_template(f"pages/{template_name}")
            rendered = template.render()

            # Write to docs/md/
            # Exception: Special handling for the Root README (language agnostic entry)
            if target_name == "ROOT_README.md":
                # Writes to repository root
                (self.root / "README.md").write_text(rendered, encoding="utf-8")
                count += 1
            else:
                # Writes to docs/md/ (e.g., README.en.md, about.md)
                (self.md_out / target_name).write_text(rendered, encoding="utf-8")
                logger.info(self.md_out / target_name)
                count += 1
        if not count:
            raise TypeError("No md pages built")

    def build_html_pages(self):
        """
        Compiles templates/pages/*.html.j2 into docs/*.html for GitHub Pages.
        """
        self._map_relationships()
        logger.info("-> Building HTML Pages...")
        # Similar logic to markdown, but targets HTML templates if they exist.
        # This aligns with the "Equal Enjoyment" goal of GHIP-001.

        pages_dir = self.templates_dir / "pages"
        logger.info(f"Templates from {pages_dir}")
        count = 0
        for template_path in pages_dir.glob("*.html.j2"):
            template_name = template_path.name
            # --- Skip the specialized skill template ---
            if template_name == "skill_detail.html.j2":
                continue
            target_name = template_name.replace(".j2", "")

            template = self.env.get_template(f"pages/{template_name}")
            rendered = template.render()

            (self.html_out / target_name).write_text(rendered, encoding="utf-8")
            count += 1
        if not count:
            raise TypeError("No html pages build")

    def build(self):
        """
        Main entry point for the build process.
        """
        self.clean()
        self._map_relationships()
        self.build_static_api()
        self.build_markdown_pages()
        self.build_html_pages()
        self.build_skill_pages()

        logger.info("Build complete.")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
