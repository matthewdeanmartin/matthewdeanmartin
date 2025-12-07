"""
builder.py
The core build engine for the README CMS.
Compiles Jinja templates + TOML data + Markdown content into final artifacts.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict

import orjson
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import HttpUrl

from .models import CMSConfig
from .config import load_config


class SiteBuilder:
    """
    Orchestrates the generation of Markdown, HTML, and Static API files.
    """

    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.src = self.root / "src"
        self.content_dir = self.src / "content"
        self.templates_dir = self.src / "readme_maker" / "templates"

        # Output directories
        self.docs_dir = self.root / "docs"
        self.md_out = self.docs_dir / "md"
        self.api_out = self.docs_dir / "apis"
        self.html_out = self.docs_dir  # HTML sits in root of docs/ for GitHub Pages

        # Load Configuration (Data Layer)
        self.config: CMSConfig = load_config(str(self.root))

        # Setup Jinja2 Environment
        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Inject Globals and Helpers
        self.env.globals["config"] = self.config
        self.env.globals["identity"] = self.config.identity
        self.env.globals["mode"] = self.config.current_mode_settings
        self.env.globals["projects"] = self.config.projects
        self.env.globals["pypi"] = self.config.pypi_packages

        # Helper to include raw markdown content from src/content/
        self.env.globals["include_content"] = self._read_content_file

    def _read_content_file(self, filename: str) -> str:
        """
        Helper for Jinja templates to pull in raw content.
        Example usage in template: {{ include_content('pages/about.md') }}
        """
        file_path = self.content_dir / filename
        if not file_path.exists():
            return f""
        return file_path.read_text(encoding="utf-8")

    def clean(self):
        """
        Cleans output directories to ensure a fresh build.
        """
        for path in [self.md_out, self.api_out]:
            if path.exists():
                shutil.rmtree(path)
            path.mkdir(parents=True, exist_ok=True)

    def build_static_api(self):
        """
        Generates the Static API (JSON) described in GHIP-001.
        """
        print("-> Building Static API...")

        # 1. Identity API
        identity_json = self.config.identity.model_dump_json(indent=2)
        (self.api_out / "identity.json").write_text(identity_json, encoding="utf-8")

        # 2. Projects API (Combines Manual + PyPI)
        projects_data = {
            "projects": [p.model_dump() for p in self.config.projects],
            "pypi": [p.model_dump() for p in self.config.pypi_packages]
        }
        # , indent=2
        def default(obj):
            if isinstance(obj, HttpUrl):
                return str(obj)
            raise TypeError
        (self.api_out / "projects.json").write_text(orjson.dumps(projects_data, default=default).decode(), encoding="utf-8")

        # 3. Mode/Config Metadata (optional but useful)
        mode_data = self.config.modes.model_dump_json(indent=2)
        (self.api_out / "config.json").write_text(mode_data, encoding="utf-8")

    def build_markdown_pages(self):
        """
        Compiles templates/pages/*.md.j2 into docs/md/*.md
        """
        print(f"-> Building Markdown Pages (Mode: {self.config.modes.current})...")

        pages_dir = self.templates_dir / "pages"
        if not pages_dir.exists():
            print("Warning: No pages templates found.")
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
                print(self.md_out / target_name)
                count += 1
        if not count:
            raise TypeError("No md pages built")

    def build_html_pages(self):
        """
        Compiles templates/pages/*.html.j2 into docs/*.html for GitHub Pages.
        """
        print("-> Building HTML Pages...")
        # Similar logic to markdown, but targets HTML templates if they exist.
        # This aligns with the "Equal Enjoyment" goal of GHIP-001.

        pages_dir = self.templates_dir / "pages"
        count = 0
        for template_path in pages_dir.glob("*.html.j2"):
            template_name = template_path.name
            target_name = template_name.replace(".j2", "")

            template = self.env.get_template(f"pages/{template_name}")
            rendered = template.render()

            (self.html_out / target_name).write_text(rendered, encoding="utf-8")
            count +=1
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
        print("Build complete.")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()