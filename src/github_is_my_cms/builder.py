# src/github_is_my_cms/builder.py
"""
The core build engine for the README CMS.
Compiles Jinja templates + TOML data + Markdown content into final artifacts.
"""

import datetime
import logging
import math
import shutil
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

        # Inject Globals and Helpers
        self.env.globals["generation"] = {"generated_at": datetime.datetime.now()}

        self.env.globals["config"] = self.config
        self.env.globals["identity"] = self.config.identity
        self.env.globals["mode"] = self.config.current_mode_settings
        self.env.globals["projects"] = self.config.projects
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
        Cross-reference Projects, Skills, and Experience.
        """
        logger.info("-> Mapping Data Relationships...")

        # 1. Initialize container for skill -> projects mapping
        self.projects_by_skill = {}
        all_projects = self.config.projects

        # 2. Iterate through every skill defined in identity.toml
        for group in self.config.identity.skills:
            for skill in group.skills:
                # Prepare a slug (e.g. "Python" -> "python", "AWS CDK" -> "aws-cdk")
                skill_slug = self._slugify(skill.name)

                matching_projects = []

                for proj in all_projects:
                    # Check A: Explicit Link in projects.toml (related_skills = ["Python"])
                    if (
                        hasattr(proj, "related_skills")
                        and skill.name in proj.related_skills
                    ):
                        matching_projects.append(proj)
                        continue

                    # Check B: Implicit Tag Match (tags = ["python"])
                    # We normalize both to lower case for comparison
                    norm_tags = [t.lower() for t in proj.tags]
                    if skill.name.lower() in norm_tags:
                        matching_projects.append(proj)

                # 3. Only if we found matches, register this skill for a page
                if matching_projects:
                    self.projects_by_skill[skill.name] = matching_projects

                    # MONKEY PATCH: We attach the slug to the Pydantic object
                    # so the templates know where to link.
                    skill.page_slug = skill_slug

    def build_skill_pages(self):
        """Generates individual HTML pages for skills."""
        logger.info("-> Building Skill Detail Pages...")

        # Check if template exists
        template_name = "pages/skill_detail.html.j2"
        if not (self.templates_dir / template_name).exists():
            logger.warning(f"Template {template_name} not found, skipping skill pages.")
            return

        template = self.env.get_template(template_name)

        # Output directory: docs/skills/
        skills_out = self.html_out / "skills"
        skills_out.mkdir(parents=True, exist_ok=True)

        if not self.projects_by_skill:
            logger.warning("No skills found")
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
        for path in [self.md_out, self.api_out]:
            if path.exists():
                shutil.rmtree(path)
            path.mkdir(parents=True, exist_ok=True)

    def build_markdown_pages(self):
        """
        Compiles templates/pages/*.md.j2 into docs/md/*.md
        """
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
        logger.info("-> Building HTML Pages...")
        # Similar logic to markdown, but targets HTML templates if they exist.
        # This aligns with the "Equal Enjoyment" goal of GHIP-001.

        pages_dir = self.templates_dir / "pages"
        logger.info(f"Templates from {pages_dir}")
        count = 0
        for template_path in pages_dir.glob("*.html.j2"):
            template_name = template_path.name
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
        self.build_static_api()
        self.build_markdown_pages()
        self.build_html_pages()
        self.build_skill_pages()

        logger.info("Build complete.")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
