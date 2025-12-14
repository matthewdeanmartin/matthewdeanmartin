"""
builder.py
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
        # TODO: this is messed up. It should be from editable installation or package.
        self.src = self.root / "src"
        self.content_dir = self.src / "content"
        self.templates_dir = self.src / "github_is_my_cms" / "templates"

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

        # Helper to include raw markdown content from src/content/
        self.env.globals["include_content"] = self._read_content_file

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

    def build_static_api(self):
        logger.info("-> Building Static API...")

        def default(obj):
            if isinstance(obj, HttpUrl):
                return str(obj)
            raise TypeError

        def write_json(path: Path, payload) -> None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                orjson.dumps(payload, default=default).decode(),
                encoding="utf-8",
            )

        def paginate(items, page_size: int):
            total = len(items)
            pages = max(1, math.ceil(total / page_size))
            for page in range(1, pages + 1):
                start = (page - 1) * page_size
                end = start + page_size
                yield page, pages, total, items[start:end]

        PAGE_SIZE = 50

        # -------- link helpers (HATEOAS) --------

        def link(href: str, rel: str = "self", type_: str = "application/json"):
            return {"rel": rel, "href": href, "type": type_}

        def links(*items):
            # keep list to preserve order & allow repeated rels
            return [i for i in items if i is not None]

        def ref_item(href: str, rel: str = "item"):
            # minimal ref object used in refs[] and rel arrays
            return {"ref": href, "rel": rel}

        # -------- base docs/apis endpoints --------
        identity_href = "/apis/identity.json"
        config_href = "/apis/config.json"

        # 1) Identity (add _links)
        identity_obj = self.config.identity.model_dump()
        identity_payload = {
            **identity_obj,
            "_links": links(
                link(identity_href, "self"),
                link("/apis/openapi.yaml", "describedby", "text/yaml"),
            ),
        }
        write_json(self.api_out / "identity.json", identity_payload)

        # 2) Config (add _links)
        config_obj = self.config.modes.model_dump()
        config_payload = {
            **config_obj,
            "_links": links(
                link(config_href, "self"),
                link("/apis/openapi.yaml", "describedby", "text/yaml"),
            ),
        }
        write_json(self.api_out / "config.json", config_payload)

        # -------- Projects + PyPI relationship indexing --------
        projects = [p.model_dump() for p in self.config.projects]
        projects_sorted = sorted(projects, key=lambda p: (p.get("slug") or "").lower())

        packages = [p.model_dump() for p in self.config.pypi_packages]
        packages_sorted = sorted(
            packages, key=lambda p: (p.get("package_name") or "").lower()
        )

        # Build mapping: github_repo ("owner/repo") -> [package_name]
        repo_to_packages = {}
        for pkg in packages_sorted:
            gr = (pkg.get("github_repo") or "").strip()
            if gr:
                repo_to_packages.setdefault(gr.lower(), []).append(pkg["package_name"])

        # Build mapping: project slug -> owner/repo (best-effort parse from repository_url)
        # Only used to create lightweight relationships; if parsing fails, relationships omitted.
        def parse_owner_repo(repo_url: str | None) -> str | None:
            if not repo_url:
                return None
            s = str(repo_url).strip()
            # Accept https://github.com/owner/repo or http://...; ignore extra segments.
            marker = "github.com/"
            idx = s.lower().find(marker)
            if idx == -1:
                return None
            tail = s[idx + len(marker) :]
            parts = [p for p in tail.split("/") if p]
            if len(parts) < 2:
                return None
            return f"{parts[0]}/{parts[1]}".lower()

        # -------- Projects endpoints --------
        projects_index_href = "/apis/projects/index.json"

        # per-project full object file (+ links + relationships)
        for p in projects_sorted:
            slug = p["slug"]
            self_href = f"/apis/projects/by-slug/{slug}.json"
            repo_key = parse_owner_repo(p.get("repository_url"))
            related_pypi = repo_to_packages.get(repo_key, []) if repo_key else []

            payload = {
                **p,
                "_links": links(
                    link(self_href, "self"),
                    link(projects_index_href, "collection"),
                    link(f"/apis/projects/pages/1.json", "first"),
                    link("/apis/openapi.yaml", "describedby", "text/yaml"),
                ),
                "_rels": {
                    # relationships are refs only (no embedded objects)
                    "pypi_packages": [
                        ref_item(f"/apis/pypi/by-name/{name}.json", "related")
                        for name in related_pypi
                    ]
                },
            }
            write_json(self.api_out / "projects" / "by-slug" / f"{slug}.json", payload)

        # list refs for projects (refs-only, but with _links + optional rel hints)
        project_refs = [
            {
                "ref": f"/apis/projects/by-slug/{p['slug']}.json",
                "rel": "item",
                # optional tiny hints; safe to remove
                "name": p.get("name"),
                "status": p.get("status"),
            }
            for p in projects_sorted
        ]

        total_projects = len(project_refs)
        total_project_pages = max(1, math.ceil(total_projects / PAGE_SIZE))

        write_json(
            self.api_out / "projects" / "index.json",
            {
                "refs": project_refs,  # still refs-only
                "meta": {
                    "type": "projects",
                    "count": total_projects,
                    "page_size": PAGE_SIZE,
                    "pages": total_project_pages,
                },
                "_links": links(
                    link(projects_index_href, "self"),
                    link(f"/apis/projects/pages/1.json", "first"),
                    link(f"/apis/projects/pages/{total_project_pages}.json", "last"),
                    link("/apis/openapi.yaml", "describedby", "text/yaml"),
                ),
            },
        )

        for page, pages, total, chunk in paginate(project_refs, PAGE_SIZE):
            page_href = f"/apis/projects/pages/{page}.json"
            prev_href = f"/apis/projects/pages/{page-1}.json" if page > 1 else None
            next_href = f"/apis/projects/pages/{page+1}.json" if page < pages else None

            write_json(
                self.api_out / "projects" / "pages" / f"{page}.json",
                {
                    "refs": chunk,
                    "meta": {
                        "type": "projects",
                        "page": page,
                        "page_size": PAGE_SIZE,
                        "pages": pages,
                        "total": total,
                    },
                    "_links": links(
                        link(page_href, "self"),
                        link(projects_index_href, "collection"),
                        link(f"/apis/projects/pages/1.json", "first"),
                        link(f"/apis/projects/pages/{pages}.json", "last"),
                        link(prev_href, "prev") if prev_href else None,
                        link(next_href, "next") if next_href else None,
                        link("/apis/openapi.yaml", "describedby", "text/yaml"),
                    ),
                },
            )

        # -------- PyPI endpoints --------
        pypi_index_href = "/apis/pypi/index.json"

        # also build inverse mapping: package_name -> github_repo -> maybe project ref
        # Make lookup from repo_key -> project slug (best effort). If multiple, keep first stable.
        repo_to_project_slug = {}
        for p in projects_sorted:
            repo_key = parse_owner_repo(p.get("repository_url"))
            if repo_key and repo_key not in repo_to_project_slug:
                repo_to_project_slug[repo_key] = p["slug"]

        for pkg in packages_sorted:
            name = pkg["package_name"]
            self_href = f"/apis/pypi/by-name/{name}.json"
            repo_key = (pkg.get("github_repo") or "").strip().lower() or None
            related_project_slug = repo_to_project_slug.get(repo_key) if repo_key else None

            payload = {
                **pkg,
                "_links": links(
                    link(self_href, "self"),
                    link(pypi_index_href, "collection"),
                    link(f"/apis/pypi/pages/1.json", "first"),
                    link("/apis/openapi.yaml", "describedby", "text/yaml"),
                ),
                "_rels": {
                    "github_project": (
                        [ref_item(f"/apis/projects/by-slug/{related_project_slug}.json", "related")]
                        if related_project_slug
                        else []
                    )
                },
            }
            write_json(self.api_out / "pypi" / "by-name" / f"{name}.json", payload)

        pypi_refs = [
            {
                "ref": f"/apis/pypi/by-name/{p['package_name']}.json",
                "rel": "item",
                # optional tiny hints; safe to remove
                "package_name": p.get("package_name"),
                "version": p.get("version"),
            }
            for p in packages_sorted
        ]

        total_pypi = len(pypi_refs)
        total_pypi_pages = max(1, math.ceil(total_pypi / PAGE_SIZE))

        write_json(
            self.api_out / "pypi" / "index.json",
            {
                "refs": pypi_refs,
                "meta": {
                    "type": "pypi",
                    "count": total_pypi,
                    "page_size": PAGE_SIZE,
                    "pages": total_pypi_pages,
                },
                "_links": links(
                    link(pypi_index_href, "self"),
                    link(f"/apis/pypi/pages/1.json", "first"),
                    link(f"/apis/pypi/pages/{total_pypi_pages}.json", "last"),
                    link("/apis/openapi.yaml", "describedby", "text/yaml"),
                ),
            },
        )

        for page, pages, total, chunk in paginate(pypi_refs, PAGE_SIZE):
            page_href = f"/apis/pypi/pages/{page}.json"
            prev_href = f"/apis/pypi/pages/{page-1}.json" if page > 1 else None
            next_href = f"/apis/pypi/pages/{page+1}.json" if page < pages else None

            write_json(
                self.api_out / "pypi" / "pages" / f"{page}.json",
                {
                    "refs": chunk,
                    "meta": {
                        "type": "pypi",
                        "page": page,
                        "page_size": PAGE_SIZE,
                        "pages": pages,
                        "total": total,
                    },
                    "_links": links(
                        link(page_href, "self"),
                        link(pypi_index_href, "collection"),
                        link(f"/apis/pypi/pages/1.json", "first"),
                        link(f"/apis/pypi/pages/{pages}.json", "last"),
                        link(prev_href, "prev") if prev_href else None,
                        link(next_href, "next") if next_href else None,
                        link("/apis/openapi.yaml", "describedby", "text/yaml"),
                    ),
                },
            )
    # def build_static_api(self):
    #     """
    #     Generates the Static API (JSON) described in GHIP-001.
    #     """
    #     print("-> Building Static API...")
    #
    #     # 1. Identity API
    #     identity_json = self.config.identity.model_dump_json(indent=2)
    #     (self.api_out / "identity.json").write_text(identity_json, encoding="utf-8")
    #
    #     # 2. Projects API (Combines Manual + PyPI)
    #     projects_data = {
    #         "projects": [p.model_dump() for p in self.config.projects],
    #         "pypi": [p.model_dump() for p in self.config.pypi_packages],
    #     }
    #
    #     # , indent=2
    #     def default(obj):
    #         if isinstance(obj, HttpUrl):
    #             return str(obj)
    #         raise TypeError
    #
    #     (self.api_out / "projects.json").write_text(
    #         orjson.dumps(projects_data, default=default).decode(), encoding="utf-8"
    #     )
    #
    #     # 3. Mode/Config Metadata (optional but useful)
    #     mode_data = self.config.modes.model_dump_json(indent=2)
    #     (self.api_out / "config.json").write_text(mode_data, encoding="utf-8")

    def build_markdown_pages(self):
        """
        Compiles templates/pages/*.md.j2 into docs/md/*.md
        """
        logger.info(f"-> Building Markdown Pages (Mode: {self.config.modes.current})...")

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
        logger.info("Build complete.")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
