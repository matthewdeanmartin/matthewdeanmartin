import datetime
import logging
import math
import shutil
from pathlib import Path

import orjson
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import HttpUrl

from .builder import SiteBuilder
from .config import load_config
from .models import CMSConfig

logger = logging.getLogger(__name__)


class SiteBuilderAPI(SiteBuilder):
    def __init__(self, root_dir: str = "."):
        super().__init__(root_dir)

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
                    link("/apis/projects/pages/1.json", "first"),
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
            related_project_slug = (
                repo_to_project_slug.get(repo_key) if repo_key else None
            )

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
                        [
                            ref_item(
                                f"/apis/projects/by-slug/{related_project_slug}.json",
                                "related",
                            )
                        ]
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

            # -------- Work Experience endpoints --------
            exp_index_href = "/apis/experience/index.json"
            exp_items = [e.model_dump() for e in self.config.work_experience]
            exp_sorted = sorted(
                exp_items,
                key=lambda e: (e.get("start_date") or "", e.get("id") or ""),
                reverse=True,
            )

            for e in exp_sorted:
                eid = e["id"]
                self_href = f"/apis/experience/by-id/{eid}.json"
                payload = {
                    **e,
                    "_links": links(
                        link(self_href, "self"),
                        link(exp_index_href, "collection"),
                        link("/apis/experience/pages/1.json", "first"),
                        link("/apis/openapi.yaml", "describedby", "text/yaml"),
                    ),
                    "_rels": {},
                }
                write_json(
                    self.api_out / "experience" / "by-id" / f"{eid}.json", payload
                )

            exp_refs = [
                {
                    "ref": f"/apis/experience/by-id/{e['id']}.json",
                    "rel": "item",
                    "organization": e.get("organization"),
                    "title": e.get("title"),
                    "end_date": e.get("end_date"),
                }
                for e in exp_sorted
            ]

            total_exp = len(exp_refs)
            total_exp_pages = max(1, math.ceil(total_exp / PAGE_SIZE))

            write_json(
                self.api_out / "experience" / "index.json",
                {
                    "refs": exp_refs,
                    "meta": {
                        "type": "experience",
                        "count": total_exp,
                        "page_size": PAGE_SIZE,
                        "pages": total_exp_pages,
                    },
                    "_links": links(
                        link(exp_index_href, "self"),
                        link("/apis/experience/pages/1.json", "first"),
                        link(f"/apis/experience/pages/{total_exp_pages}.json", "last"),
                        link("/apis/openapi.yaml", "describedby", "text/yaml"),
                    ),
                },
            )

            for page, pages, total, chunk in paginate(exp_refs, PAGE_SIZE):
                page_href = f"/apis/experience/pages/{page}.json"
                prev_href = (
                    f"/apis/experience/pages/{page - 1}.json" if page > 1 else None
                )
                next_href = (
                    f"/apis/experience/pages/{page + 1}.json" if page < pages else None
                )

                write_json(
                    self.api_out / "experience" / "pages" / f"{page}.json",
                    {
                        "refs": chunk,
                        "meta": {
                            "type": "experience",
                            "page": page,
                            "page_size": PAGE_SIZE,
                            "pages": pages,
                            "total": total,
                        },
                        "_links": links(
                            link(page_href, "self"),
                            link(exp_index_href, "collection"),
                            link("/apis/experience/pages/1.json", "first"),
                            link(f"/apis/experience/pages/{pages}.json", "last"),
                            link(prev_href, "prev") if prev_href else None,
                            link(next_href, "next") if next_href else None,
                            link("/apis/openapi.yaml", "describedby", "text/yaml"),
                        ),
                    },
                )

            # -------- Resumes endpoints --------
            res_index_href = "/apis/resumes/index.json"
            res_items = [r.model_dump() for r in self.config.resumes]
            res_sorted = sorted(
                res_items,
                key=lambda r: (
                    r.get("status") != "active",
                    r.get("valid_from") or "",
                    r.get("id") or "",
                ),
                reverse=True,
            )

            for r in res_sorted:
                rid = r["id"]
                self_href = f"/apis/resumes/by-id/{rid}.json"
                payload = {
                    **r,
                    "_links": links(
                        link(self_href, "self"),
                        link(res_index_href, "collection"),
                        link("/apis/resumes/pages/1.json", "first"),
                        link("/apis/openapi.yaml", "describedby", "text/yaml"),
                    ),
                    "_rels": {},
                }
                write_json(self.api_out / "resumes" / "by-id" / f"{rid}.json", payload)

            res_refs = [
                {
                    "ref": f"/apis/resumes/by-id/{r['id']}.json",
                    "rel": "item",
                    "label": r.get("label"),
                    "status": r.get("status"),
                    "format": r.get("format"),
                }
                for r in res_sorted
            ]

            total_res = len(res_refs)
            total_res_pages = max(1, math.ceil(total_res / PAGE_SIZE))

            write_json(
                self.api_out / "resumes" / "index.json",
                {
                    "refs": res_refs,
                    "meta": {
                        "type": "resumes",
                        "count": total_res,
                        "page_size": PAGE_SIZE,
                        "pages": total_res_pages,
                    },
                    "_links": links(
                        link(res_index_href, "self"),
                        link("/apis/resumes/pages/1.json", "first"),
                        link(f"/apis/resumes/pages/{total_res_pages}.json", "last"),
                        link("/apis/openapi.yaml", "describedby", "text/yaml"),
                    ),
                },
            )

            for page, pages, total, chunk in paginate(res_refs, PAGE_SIZE):
                page_href = f"/apis/resumes/pages/{page}.json"
                prev_href = f"/apis/resumes/pages/{page - 1}.json" if page > 1 else None
                next_href = (
                    f"/apis/resumes/pages/{page + 1}.json" if page < pages else None
                )

                write_json(
                    self.api_out / "resumes" / "pages" / f"{page}.json",
                    {
                        "refs": chunk,
                        "meta": {
                            "type": "resumes",
                            "page": page,
                            "page_size": PAGE_SIZE,
                            "pages": pages,
                            "total": total,
                        },
                        "_links": links(
                            link(page_href, "self"),
                            link(res_index_href, "collection"),
                            link("/apis/resumes/pages/1.json", "first"),
                            link(f"/apis/resumes/pages/{pages}.json", "last"),
                            link(prev_href, "prev") if prev_href else None,
                            link(next_href, "next") if next_href else None,
                            link("/apis/openapi.yaml", "describedby", "text/yaml"),
                        ),
                    },
                )
