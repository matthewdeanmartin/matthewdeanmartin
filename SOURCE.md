## Tree for 
```
├── .github/
│   └── workflows/
│       └── deploy.yml
├── AGENT.md
├── data_sample/
│   ├── identity.toml
│   ├── projects.toml
│   ├── pypi_projects.toml
│   ├── readme_cms.toml
│   ├── resumes.toml
│   └── work_experience.toml
├── Makefile
├── pyproject.toml
├── readme_cms.toml
├── SOURCE_DATA.md
└── src/
    ├── GHIP_001_Specification.md
    └── github_is_my_cms/
        ├── builder.py
        ├── builder_api.py
        ├── cli.py
        ├── config.py
        ├── data_sources.py
        └── models.py
```

## File: AGENT.md
```markdown
All libraries will be installed. DO NOT ADD if-blocks around imports to provide fallbacks if a library fails to import.

Always type annotate your python code.

Prefer Pathlib over non-pathlib solution, i.e. avoid using str Paths.
```
## File: Makefile
```
format:
	isort src
	black src
	mdformat src docs *.md

data:
	uv run gimc update-data

build:
	uv run gimc build

everything: data build format
	echo "everything"
	cp docs/md/README.en.md README.en.md
```
## File: pyproject.toml
```
[project]
name = "github-is-my-cms"
version = "0.1.0"
description = "A Multi-Page GitHub README CMS"
readme = "README.md"
requires-python = ">=3.14"
license = { text = "MIT" }
authors = [
    { name = "Matthew Dean Martin", email = "matthew.dean.martin@gmail.com" }
]
keywords = ["github", "readme", "cms", "documentation", "generator", "static-site"]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.14",
    "Topic :: Documentation",
    "Topic :: Software Development :: Documentation",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Text Processing :: Markup :: Markdown",
    "Typing :: Typed",
]

dependencies = [
    # models
    "pydantic>=2.0",
    # templating engine
    "jinja2>=3.1.0",
    # speed
    "orjson",
    # config
    "tomli-w",
    # ready pypi
    "httpx",
    "beautifulsoup4",
    # pretty build output
    "colorlog", # could be optional
]

[project.scripts]
gimc = "github_is_my_cms.cli:main"
github-is-my-cms = "github_is_my_cms.cli:main"


[dependency-groups]
dev = [
    "pre-commit",
    "proselint",
    "mdformat",
    "linkcheckmd",
    "typing_extensions",
    "troml-dev-status>0.5.0",
    "jiggle_version",
    "cffi",
    "pytest-asyncio",
    "httpie",
    "pytest>=6.0.1",
    "pytest-cov>=2.10.1",
    "pytest-timeout>=2.4.0",
    "pylint",

    "git2md; python_version >= '3.10'",
    "pyclean; python_version >= '3.12'",
    "strip-docs>=1.0; python_version >= '3.12'",

    "gha-update; python_version >= '3.12'",
    "mkdocstrings[python]",
    "mkdocs; python_version >= '3.12'",
    "mdformat",


    # plugin finder
    "packaging; python_version >= '3.8'",

    # mpy
    "mypy; python_version >= '3.8'",
    "types-toml; python_version >= '3.8'",
    "types-requests",

    # reports

    # build
    "vermin; python_version >= '3.8'",
    "metametameta>=0.1.3; python_version >= '3.9'",
    "hatchling; python_version >= '3.8'",
    "ruff>=0.12.0; python_version >= '3.8'",
    "pylint; python_version >= '3.8'",

    # testing tools
    "pytest; python_version >= '3.8'",
    "pytest-cov; python_version >= '3.8'",
    "pytest-xdist>=3.5.0; python_version >= '3.8'",
    "pytest-randomly>=3.15.0; python_version >= '3.8'",
    "pytest-sugar>=0.9.7; python_version >= '3.8'",
    "pytest-mock; python_version >= '3.8'",
    "pytest-unused-fixtures; python_version >= '3.10'",
    "hypothesis[cli]; python_version >= '3.8'",
    "detect-test-pollution",

    # docs
    "interrogate>=1.5.0; python_version >= '3.8'",
    "pydoctest==0.2.1; python_version >= '3.8'",
    "pdoc3>=0.5.0; python_version >= '3.8'",
    "mdformat>=0.5.0; python_version >= '3.8'",
    "linkcheckmd>=1.4.0; python_version >= '3.8'",
    "codespell>=2.2.6; python_version >= '3.8'",
    "pyenchant>=3.2.2; python_version >= '3.8'",
]

[tool.ruff]
line-length = 200

[tool.mypy]
ignore_missing_imports = true
strict = true

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/github_is_my_cms"]
include = [
    "src/github_is_my_cms/**/*.py",
    "src/github_is_my_cms/py.typed",
    "/README.md", "LICENSE",
]

[tool.hatch.build.targets.sdist]
include = [
    "src/github_is_my_cms/**/*.py",
    "src/github_is_my_cms/py.typed",
    "/README.md", "LICENSE",
]
```
## File: readme_cms.toml
```
# src/github_is_my_cms/data/readme_cms.toml
theme = "professional"

[mode]
# Options: "job_hunting", "project_promotion", "self_promotion"
# current = "project_promotion"
current = "job_hunting"
# current = "self_promotion"

[mode.job_hunting]
enable_projects = true
project_visibility = "curated"
resume_url = "https://matthewdeanmartin.github.io/matthewdeanmartin"

[mode.project_promotion]
enable_projects = true
project_visibility = "full"
highlight_pypi = true

[mode.self_promotion]
enable_talks = true
enable_posts = true
highlight_blog = true

[languages]
default = "en"
supported = ["en"]
```
## File: SOURCE_DATA.md
```markdown
## Tree for 
```
├── AGENT.md
├── data_sample/
│   ├── identity.toml
│   ├── projects.toml
│   ├── pypi_projects.toml
│   ├── readme_cms.toml
│   ├── resumes.toml
│   └── work_experience.toml
├── readme_cms.toml
└── src/
    └── github_is_my_cms/
        ├── builder.py
        ├── cli.py
        ├── config.py
        ├── data_sources.py
        ├── models.py
        └── templates/
            └── professional/
                ├── components/
                │   └── identity_graph.md.j2
                ├── layouts/
                │   ├── master.html.j2
                │   └── master.md.j2
                └── pages/
                    ├── index.html.j2
                    ├── projects.html.j2
                    ├── projects.md.j2
                    ├── README.en.md.j2
                    └── skill_detail.html.j2
```

## File: AGENT.md
```markdown
All libraries will be installed. DO NOT ADD if-blocks around imports to provide fallbacks if a library fails to import.

Always type annotate your python code.

Prefer Pathlib over non-pathlib solution, i.e. avoid using str Paths.
```
## File: readme_cms.toml
```
# src/github_is_my_cms/data/readme_cms.toml
theme = "professional"

[mode]
# Options: "job_hunting", "project_promotion", "self_promotion"
# current = "project_promotion"
# current = "job_hunting"
# current = "self_promotion"

[mode.job_hunting]
enable_projects = true
project_visibility = "curated"
resume_url = "https://matthewdeanmartin.github.io/matthewdeanmartin"

[mode.project_promotion]
enable_projects = true
project_visibility = "full"
highlight_pypi = true

[mode.self_promotion]
enable_talks = true
enable_posts = true
highlight_blog = true

[languages]
default = "en"
supported = ["en"]
```
## File: data_sample\identity.toml
```
# src/github_is_my_cms/data/identity.toml

name = "Matthew Dean Martin"
tagline = "Pythonist, Devops Guy, and Govtech Specialist"
location = "United States"
pypi_username = "matthewdeanmartin"
github_username =  "matthewdeanmartin"

[content]
skills_intro = "I used to be a full stack developer, I evolved into tech lead and most recently devops work. I write code and know how to ship in a govtech environment."
projects_intro = "Here is a collection of my manual projects and published PyPI packages."
job_hunting_intro = "I am currently looking for new opportunities. My focus is on production-quality backend systems."

# --- Resumes ---
[[resumes]]
label = "Resume from 2015"
url = "https://matthewdeanmartin.github.io/"
icon = "📄"

[[resumes]]
label = "Novelty Resume from 2024"
url = "https://matthewdeanmartin.github.io/resume/browser/"
description = "Hire button and a fire button!"
icon = "📄"

# --- Talks ---
[[talks]]
title = "Python Librarian"
url = "https://www.youtube.com/channel/UCw1p2a3LW1VG7DTZQaT8Oaw"
icon = "▶️"

# --- Skills ---
# Column 1
[[skills]]
category = "Devops"
[[skills.skills]]
name = "Typescript for AWS CDK"
level = "Expert"
icon = "🌐"
[[skills.skills]]
name = "Terraform for AWS / HCL"
level = "Expert"
icon = "🪐"
[[skills.skills]]
name = "Go for Terratest"
level = "Good enough"
icon = "🐹"

# Column 2
[[skills]]
category = "Backend Development"
[[skills.skills]]
name = "Python for Serverless in AWS"
level = "Expert"
icon = "🐍"
[[skills.skills]]
name = "Postgres"
icon = "🐘"
[[skills.skills]]
name = "DynamoDB"
icon = "🗄️"

# Column 3
[[skills]]
category = "Build Master"
[[skills.skills]]
name = "Gitlab Pipelines"
level = "Expert"
icon = "🦊"
[[skills.skills]]
name = "Bash for Gitlab"
level = "Very Good"
icon = "`>_`"

# --- Profiles (Backlinks) ---

# Group: Social Media with Backlinks
[[profiles]]
service = "Mastodon"
handle = "mastodon.social/@mistersql"
url = "https://mastodon.social/@mistersql"
group = "social"
icon = "🐘"

[[profiles]]
service = "BlueSky"
handle = "bsky.app"
url = "https://bsky.app/profile/mistersql.bsky.social"
group = "social"
icon = "🦋"

[[profiles]]
service = "LinkedIn"
handle = "LinkedIn"
url = "https://linkedin.com/in/matthewdeanmartin"
group = "social"
icon = "🔗"


# Group: Verified Profile Pages
[[profiles]]
service = "Dev.to"
handle = "dev.to"
url = "https://dev.to/matthewdeanmartin"
group = "verified"
icon = "💻"

[[profiles]]
service = "Gravatar"
handle = "Gravatar"
url = "https://gravatar.com/matthewdmartin"
group = "verified"
icon = "🌀"

[[profiles]]
service = "StackOverflow"
handle = "StackOverflow"
url = "https://stackoverflow.com/users/33264/matthewmartin"
group = "verified"
icon = "🔥"
```
## File: data_sample\projects.toml
```
# src/github_is_my_cms/data/projects.toml

[[projects]]
slug = "Hicmah"
name = "Hicmah"
description = "Hicmah - Hit Counter Module and Handler"
url = "https://github.com/matthewdeanmartin/Hicmah"
repository_url = "https://github.com/matthewdeanmartin/Hicmah"
tags = [
    "analytics",
    "handler",
    "hit-counter",
    "javascript",
    "module",
    "web-development",
]
status = "active"
related_skills = ["AWS", "Serverless"]

[projects.cms]
suppress = false
package_links = []
```
## File: data_sample\pypi_projects.toml
```
# src/github_is_my_cms/data/pypi_projects.toml

[[packages]]
package_name = "dedlin"
github_repo = "matthewdeanmartin/dedlin"
version = "1.0.0"
summary = "A modern python port of the classic edlin line editor."
downloads_monthly = 543
docs_url = "https://dedlin.readthedocs.io"
last_updated = "2024-11-20"

[[packages]]
package_name = "cli_tool_audit"
github_repo = "matthewdeanmartin/cli_tool_audit"
version = "0.4.2"
summary = "Audit your CLI tools for version and existence."
downloads_monthly = 1200
last_updated = "2024-10-15"
```
## File: data_sample\readme_cms.toml
```
# src/github_is_my_cms/data/readme_cms.toml
theme = "professional"

[mode]
# Options: "job_hunting", "project_promotion", "self_promotion"
current = "project_promotion"

[mode.job_hunting]
enable_projects = true
project_visibility = "curated"
resume_url = "https://matthewdeanmartin.github.io/matthewdeanmartin"

[mode.project_promotion]
enable_projects = true
project_visibility = "full"
highlight_pypi = true

[mode.self_promotion]
enable_talks = true
enable_posts = true
highlight_blog = true

[languages]
default = "en"
supported = ["en"]
```
## File: data_sample\resumes.toml
```
# data/resumes.toml

[[resumes]]
id = "resume-2015"
label = "Resume from 2015"
url = "https://matthewdeanmartin.github.io/"
format = "html"          # pdf | docx | html | md | other
audience = "general"
status = "expired"       # active | expired | draft
valid_from = "2015-01"
icon = "📄"

[[resumes]]
id = "resume-2024-novelty"
label = "Novelty Resume from 2024"
url = "https://matthewdeanmartin.github.io/resume/browser/"
format = "html"
audience = "general"
status = "active"
valid_from = "2024-01"
description = "Hire button and a fire button!"
icon = "📄"
```
## File: data_sample\work_experience.toml
```
# data/work_experience.toml

[[experience]]
id = "acme-2021-2024"
organization = "Acme Corp"
title = "Senior Platform Engineer"
employment_type = "full_time" # full_time | contract | freelance | volunteer
start_date = "2021-06"
end_date = "2024-11"         # or "present"
location = "Remote"
summary = "Owned CI/CD, platform observability, and infra automation for regulated workloads."

responsibilities = [
  "Built multi-account AWS landing zone with policy-as-code.",
  "Reduced deploy time from 40m to 10m via pipeline refactors.",
]

technologies = ["AWS", "Terraform", "Python", "Postgres"]
links = [
  { label = "Company", url = "https://example.com" }
]

related_project_slugs = ["Hicmah", "dedlin"]
```
## File: src\github_is_my_cms\builder.py
```python
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
```
## File: src\github_is_my_cms\cli.py
```python
# src/github_is_my_cms/cli.py
"""
Command-line interface for the github-is-my-cms.
Handles argument parsing, logging setup, and command dispatch.
"""

import argparse
import logging
import logging.config
import sys
from pathlib import Path
from typing import List, Optional

import github_is_my_cms.__about__ as __about__
from github_is_my_cms.builder_api import SiteBuilderAPI
from github_is_my_cms.logging_config import generate_config

# Import the builder
from .builder import SiteBuilder
from .data_sources import DataUpdater

# Versioning
# TODO: ideally fetched from package metadata in production
VERSION = __about__.__version__

logger = logging.getLogger(__name__)


def setup_logging(level_name: str):
    """
    Configures the root logger based on the user's verbosity selection.
    """
    numeric_level = getattr(logging, level_name.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level_name}")
    print(level_name)
    logging.config.dictConfig(generate_config(level=level_name))
    logger.debug("Testing 1123")
    # logging.basicConfig(
    #     level=numeric_level,
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #     datefmt="%H:%M:%S",
    # )


def cmd_build(args: argparse.Namespace):
    """
    Handler for the 'build' subcommand.
    Compiles Markdown and HTML pages.
    """
    logging.info("Starting build process...")
    try:
        builder = SiteBuilder(root_dir=args.root)
        api_builder = SiteBuilderAPI(root_dir=args.root)
        builder.clean()
        api_builder.build_static_api()
        builder.build_markdown_pages()
        builder.build_html_pages()
        logging.info("Build completed successfully.")
    except Exception as e:
        logging.error(f"Build failed: {e}", exc_info=True)
        sys.exit(1)


def cmd_lint(args: argparse.Namespace):
    """
    Placeholder: Validates content structure, links, and TOML data.
    """
    logging.warning("Command 'lint' is not yet implemented.")
    logging.info(f"Would scan root: {args.root}")
    # TODO: Implement quality checks defined in GHIP-001 "Quality Checks"


def cmd_translate(args: argparse.Namespace):
    """
    Placeholder: Runs LLM-based translation for non-default languages.
    """
    logging.warning("Command 'translate' is not yet implemented.")
    # TODO: Implement LLM integration defined in GHIP-001 "Translation Workflow"


def cmd_update_data(args: argparse.Namespace):
    """
    Fetches fresh data from PyPI and updates the local TOML files.
    """
    logging.info("Starting data update...")

    if DataUpdater is None:
        logging.error("DataUpdater module not found.")
        sys.exit(1)

    root_path = Path(args.root)
    updater = DataUpdater(root_dir=root_path)

    try:
        # 1. Update GitHub Projects (Source of Truth)
        updater.update_projects_from_github()

        # 2. Update PyPI Metadata (Supplementary)
        updater.update_pypi_data()
        logging.info("Data update completed.")
    except Exception as e:
        logging.error(f"Update failed: {e}", exc_info=True)
        sys.exit(1)


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="github-is-my-cms, a github centric profile and readme generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # --- Global Arguments ---
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        "--log-level",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging verbosity.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Path to the repository root containing readme_cms.toml.",
    )

    # --- Subcommands ---
    subparsers = parser.add_subparsers(
        title="Commands", dest="command", help="Available operations"
    )

    # Command: build
    parser_build = subparsers.add_parser(
        "build", help="Compile TOML and Markdown into final docs/ artefacts."
    )
    parser_build.set_defaults(func=cmd_build)

    # Command: lint (Placeholder)
    parser_lint = subparsers.add_parser(
        "lint", help="Validate links, content structure, and data integrity."
    )
    parser_lint.set_defaults(func=cmd_lint)

    # Command: translate (Placeholder)
    parser_translate = subparsers.add_parser(
        "translate", help="Regenerate translations using configured LLM provider."
    )
    parser_translate.set_defaults(func=cmd_translate)

    # Command: update-data (Placeholder)
    parser_update = subparsers.add_parser(
        "update-data", help="Refresh cached data from PyPI and GitHub APIs."
    )
    parser_update.set_defaults(func=cmd_update_data)

    # --- Execution Logic ---

    # Check for empty args (excluding script name) to default to help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(argv)

    # Apply logging configuration
    setup_logging(args.log_level)

    # Dispatch to function
    if hasattr(args, "func"):
        args.func(args)
    else:
        # Fallback if valid command structure but no func mapped (unlikely with subparsers)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```
## File: src\github_is_my_cms\config.py
```python
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
```
## File: src\github_is_my_cms\data_sources.py
```python
"""
data_sources.py
Handles fetching external data from PyPI and GitHub APIs to update local TOML caches.
"""

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

import httpx
import tomli_w
from bs4 import BeautifulSoup

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

    BASE_URL = "https://pypi.org/user"

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
                    logger.info(
                        f"PyPI: Using cached package list for user '{username}'."
                    )
                    return data.get("packages", [])
            except json.JSONDecodeError:
                pass

        # 2. Fetch via HTTPX + BS4
        logger.info(
            f"PyPI: Discovering packages for user '{username}' via HTML scraping..."
        )

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
                package_names = sorted(
                    list(set(s.get_text(strip=True) for s in snippets))
                )

            # 3. Save Cache
            cache_payload = {
                "user": username,
                "timestamp": datetime.now().isoformat(),
                "packages": package_names,
            }
            self.cache_file.write_text(
                json.dumps(cache_payload, indent=2), encoding="utf-8"
            )

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
            req = urllib.request.Request(
                url, headers={"User-Agent": "github-is-my-cms/0.1.0"}
            )
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
                    "github_repo": self._extract_github_repo(
                        info.get("project_urls") or {}
                    ),
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
            logger.warning(
                "Could not load full config; some auto-discovery features may fail."
            )
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
        pkg_map = {
            p["package_name"]: p for p in existing_packages if "package_name" in p
        }

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
            logger.info(
                "No pypi_username configured in identity.toml. Skipping auto-discovery."
            )

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

        logger.info(
            f"Successfully updated {self.pypi_file} with {len(updated_list)} packages."
        )
```
## File: src\github_is_my_cms\models.py
```python
"""
models.py
Data structures for the github-is-my-cms.
Implements schema validation and JSON serialization for the Static API.
"""

from __future__ import annotations

import itertools
import logging
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

logger = logging.getLogger(__name__)
# --- Enums ---


class SiteMode(str, Enum):
    """The three operational modes defined in GHIP-001."""

    JOB_HUNTING = "job_hunting"
    PROJECT_PROMOTION = "project_promotion"
    SELF_PROMOTION = "self_promotion"


class ProjectVisibility(str, Enum):
    """Controls how much detail is shown for projects in different modes."""

    CURATED = "curated"
    MINIMAL = "minimal"
    FULL = "full"


# --- New Models for Skills & Resumes ---


class Skill(BaseModel):
    name: str
    level: Optional[str] = None  # e.g. "Expert", "Very Good"
    icon: Optional[str] = None  # e.g. "🌐", "🐍"

    def display(self) -> str:
        parts = []
        if self.icon:
            parts.append(self.icon)
        parts.append(self.name)
        if self.level:
            parts.append(f"- {self.level}")
        return " ".join(parts)


class SkillGroup(BaseModel):
    category: str  # Header, e.g. "Devops"
    skills: List[Skill] = []


class ResumeEntry(BaseModel):
    label: str  # "Resume from 2015"
    url: HttpUrl
    description: Optional[str] = None  # "Hire button and a fire button!"
    icon: str = "📄"


class TalkEntry(BaseModel):
    title: str
    url: HttpUrl
    icon: str = "▶️"


# --- Identity Models ---


class SocialProfile(BaseModel):
    """
    Represents a node in the Identity Graph.
    """

    service: str = Field(
        ..., description="Name of the service (e.g., github, linkedin)"
    )
    handle: str = Field(..., description="Username or handle")
    url: HttpUrl = Field(..., description="Link to the profile")
    group: str = Field("social", description="Group key: 'social' or 'verified'")
    same_as: List[HttpUrl] = Field(
        default_factory=list, description="List of equivalent URLs for JSON-LD"
    )
    icon: Optional[str] = None  # e.g. "🌐", "🐍"

    @field_validator("url", "service")
    @classmethod
    def validate_no_twitter(cls, v: Any, info) -> Any:
        """
        GHIP-001 Quality Check: Strictly forbid Twitter/X.
        """
        forbidden = ["twitter.com", "x.com"]
        val_str = str(v).lower()
        if any(f in val_str for f in forbidden):
            raise ValueError(f"Twitter/X links are strictly forbidden by GHIP-001: {v}")
        return v


class IdentityContent(BaseModel):
    skills_intro: Optional[str] = None
    projects_intro: Optional[str] = None
    job_hunting_intro: Optional[str] = None


class Identity(BaseModel):
    """
    Core personal information and aggregation of the identity graph.
    """

    name: str
    tagline: str
    location: Optional[str] = None
    email: Optional[str] = None

    pypi_username: Optional[str] = Field(
        None, description="Username on PyPI to auto-discover packages"
    )
    github_username: Optional[str] = Field(
        None, description="Username on GitHub to filter repos"
    )

    profiles: List[SocialProfile] = Field(
        default_factory=list, description="The Identity Graph"
    )

    resumes: List[ResumeEntry] = Field(default_factory=list)
    skills: List[SkillGroup] = Field(default_factory=list)
    talks: List[TalkEntry] = Field(default_factory=list)

    content: IdentityContent = Field(default_factory=IdentityContent)

    @property
    def skill_rows(self) -> List[List[str]]:
        """
        Helper to transpose columns (Categories) into Markdown Table Rows.
        Returns a list of rows, where each row is a list of strings (cells).
        """
        if not self.skills:
            return []

        # Get list of skill-lists: [[s1, s2], [s3, s4], [s5]]
        columns = [group.skills for group in self.skills]
        # zip_longest fills missing items with None
        rows = itertools.zip_longest(*columns, fillvalue=None)

        rendered_rows = []
        for row in rows:
            # Render each cell
            rendered_row = []
            for item in row:
                if item:
                    rendered_row.append(item.display())
                else:
                    rendered_row.append("")
            rendered_rows.append(rendered_row)
        return rendered_rows


# --- Project Models ---


class CMSDirective(BaseModel):
    suppress: bool = False
    package_links: List[HttpUrl] = []


class Project(BaseModel):
    """
    A manually curated project entry (from projects.toml).
    """

    slug: str = Field(..., description="Unique identifier for the project")
    name: str
    description: str
    url: Optional[HttpUrl] = None
    repository_url: Optional[HttpUrl] = None
    tags: List[str] = Field(default_factory=list)
    featured: bool = False
    status: str = Field("active", description="active, archived, or maintenance")

    cms: Optional[CMSDirective] = None

    related_skills: List[str] = Field(default_factory=list)


class SkillPageContext(BaseModel):
    skill: Skill
    projects: List[Project]
    slug: str


class PyPIPackage(BaseModel):
    """
    Auto-generated metadata from PyPI (from pypi_projects.toml).
    """

    package_name: str
    github_repo: Optional[str] = Field(None, description="owner/repo format")
    version: Optional[str] = None
    summary: Optional[str] = None
    downloads_monthly: Optional[int] = 0
    docs_url: Optional[HttpUrl] = None
    last_updated: Optional[str] = None


# --- Configuration & Mode Models ---


class JobHuntingSettings(BaseModel):
    enable_projects: bool = True
    project_visibility: ProjectVisibility = ProjectVisibility.CURATED
    highlight_skills: bool = True
    resume_url: Optional[HttpUrl] = None


class ProjectPromotionSettings(BaseModel):
    enable_projects: bool = True
    project_visibility: ProjectVisibility = ProjectVisibility.FULL
    highlight_pypi: bool = True


class SelfPromotionSettings(BaseModel):
    enable_talks: bool = True
    enable_posts: bool = True
    highlight_blog: bool = True


class ModeConfig(BaseModel):
    """
    Configuration container for mode-specific behaviors.
    """

    current: SiteMode = SiteMode.PROJECT_PROMOTION
    job_hunting: JobHuntingSettings = Field(default_factory=JobHuntingSettings)
    project_promotion: ProjectPromotionSettings = Field(
        default_factory=ProjectPromotionSettings
    )
    self_promotion: SelfPromotionSettings = Field(default_factory=SelfPromotionSettings)


class LanguageConfig(BaseModel):
    default: str = "en"
    supported: List[str] = ["en"]


# --- Root CMS Model ---


class CMSConfig(BaseModel):
    """
    The aggregate model representing the entire state of the CMS.
    This maps to the logical structure of the TOML files combined.
    """

    identity: Identity
    modes: ModeConfig = Field(default_factory=ModeConfig)
    languages: LanguageConfig = Field(default_factory=LanguageConfig)
    projects: List[Project] = Field(default_factory=list)
    pypi_packages: List[PyPIPackage] = Field(default_factory=list)
    theme: Optional[str] = "default"

    work_experience: List[WorkExperienceEntry] = Field(default_factory=list)
    resumes: List[ResumeArtifact] = Field(default_factory=list)

    @property
    def featured_resume_url(self) -> Optional[str]:
        for r in self.resumes:
            if r.status == ResumeStatus.ACTIVE:
                return str(r.url)
        return None

    @property
    def current_mode_settings(self):
        """Helper to retrieve settings for the currently active mode."""
        if self.modes.current == SiteMode.JOB_HUNTING:
            return self.modes.job_hunting
        elif self.modes.current == SiteMode.PROJECT_PROMOTION:
            return self.modes.project_promotion
        elif self.modes.current == SiteMode.SELF_PROMOTION:
            return self.modes.self_promotion
        return self.modes.project_promotion


# --- add near other enums ---


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    VOLUNTEER = "volunteer"


class ResumeStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    DRAFT = "draft"


class ResumeFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    MD = "md"
    OTHER = "other"


class LabeledLink(BaseModel):
    label: str
    url: HttpUrl


class WorkExperienceEntry(BaseModel):
    id: str
    organization: str
    title: str
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    start_date: str  # "YYYY-MM" or "YYYY"
    end_date: str  # "YYYY-MM" or "present"
    location: Optional[str] = None
    summary: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    links: List[LabeledLink] = Field(default_factory=list)

    related_project_slugs: List[str] = Field(default_factory=list)
    # We will inject the actual Project objects here during the build step
    linked_projects: List[Project] = Field(default_factory=list, exclude=True)


class ResumeArtifact(BaseModel):
    id: str
    label: str
    url: HttpUrl
    format: ResumeFormat = ResumeFormat.PDF
    audience: Optional[str] = None
    status: ResumeStatus = ResumeStatus.ACTIVE
    valid_from: Optional[str] = None  # "YYYY-MM" or "YYYY"
    valid_until: Optional[str] = None  # optional
    description: Optional[str] = None
    icon: Optional[str] = "📄"
```
## File: src\github_is_my_cms\templates\professional\components\identity_graph.md.j2
```
### Connect

{% for profile in identity.profiles %}
* **{{ profile.service|title }}**: [{{ profile.handle }}]({{ profile.url }})
{%- endfor %}

{% if config.modes.current == "job_hunting" and config.modes.job_hunting.resume_url %}
* **Resume**: [Download PDF]({{ config.modes.job_hunting.resume_url }})
{% endif %}
```
## File: src\github_is_my_cms\templates\professional\layouts\master.html.j2
```
<!DOCTYPE html>
<html lang="{{ config.languages.default }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ identity.name }} - Resume</title>
    <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #333333;
            --link-color: #0056b3;
            --border-color: #dddddd;
        }
        body {
            font-family: "Georgia", "Times New Roman", Times, serif;
            line-height: 1.4;
            color: var(--text-color);
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--bg-color);
        }
        a { color: var(--link-color); text-decoration: none; }
        a:hover { text-decoration: underline; }

        /* Typography */
        h1 { margin: 0; font-size: 2.2rem; text-transform: uppercase; letter-spacing: 1px; }
        h2 { margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.1rem; text-transform: uppercase; border-bottom: 2px solid #333; padding-bottom: 2px; }
        h3 { margin-top: 1rem; margin-bottom: 0.25rem; font-size: 1rem; font-weight: bold; }
        p { margin: 0.5rem 0; }

        /* Header / Nav */
        header { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; margin-bottom: 1.5rem; }
        .header-info { text-align: right; font-size: 0.9rem; }
        .nav-links a { margin-left: 10px; font-family: sans-serif; font-size: 0.85rem; color: #666; }

        /* Tables */
        table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; font-size: 0.95rem; }
        th, td { text-align: left; padding: 6px 4px; border-bottom: 1px solid #eee; vertical-align: top;}
        th { font-weight: bold; border-bottom: 2px solid #aaa; }

        /* Lists */
        ul { margin: 0.5rem 0; padding-left: 1.2rem; }
        li { margin-bottom: 0.2rem; }

        /* Utility */
        .meta { color: #666; font-size: 0.85rem; font-style: italic; }
        .tags { font-family: sans-serif; font-size: 0.75rem; color: #555; }
        .right { float: right; }

        @media print {
            body { padding: 0; }
            .nav-links { display: none; }
            a[href]:after { content: none !important; }
        }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>{{ identity.name }}</h1>
            <div class="meta">{{ identity.tagline }}</div>
        </div>
        <div class="header-info">
            <div>{{ identity.location }}</div>
            <div>
                {% for profile in identity.profiles if profile.group == 'social' %}
                <a href="{{ profile.url }}">{{ profile.service }}</a>{% if not loop.last %} | {% endif %}
                {% endfor %}
            </div>
            <div class="nav-links">
                <a href="index.html">Resume</a>
                <a href="projects.html">Projects List</a>
                <a href="swagger/index.html">API</a>
            </div>
        </div>
    </header>

    <main>
        {% block body %}{% endblock %}
    </main>

    <footer>
        <div style="text-align: center; font-size: 0.7rem; margin-top: 3rem; color: #999;">
            Last Updated: {{ generation.generated_at }} &mdash; Mode: {{ mode.current }}
        </div>
    </footer>
</body>
</html>
```
## File: src\github_is_my_cms\templates\professional\layouts\master.md.j2
```
# {{ identity.name }}
{{ identity.tagline }} | {{ identity.location }}
[Home](../../README.md) • [Projects](projects.md) • [API](../apis/openapi.yaml)

---

{% block body %}{% endblock %}

---
*Generated by github-is-my-cms | {{ generation.generated_at }}*
```
## File: src\github_is_my_cms\templates\professional\pages\index.html.j2
```
{% extends "layouts/master.html.j2" %}

{% block body %}

    <section>
        <h2>Professional Summary</h2>
        <article>
            {{ include_content('pages/about.md') }}
        </article>
    </section>

    <section>
        <h2>Skills</h2>
        <table>
            {% for group in identity.skills %}
                <tr>
                    <td style="width: 25%; font-weight: bold;">{{ group.category }}</td>
                    <td>
                        {% for skill in group.skills %}
                            {% if skill.page_slug %}
                                {# Link to the generated skill page #}
                                <a href="skills/{{ skill.page_slug }}.html">{{ skill.name }}</a>
                            {% else %}
                                {{ skill.name }}
                            {% endif %}

                            {% if skill.level %} <span class="meta">({{ skill.level }})</span>{% endif %}
                            {% if not loop.last %}, {% endif %}
                        {% endfor %}
                    </td>
                </tr>
            {% endfor %}
        </table>
    </section>

    {% if config.modes.current == "job_hunting" %}
        <section>
            <h2>Work Experience</h2>

            {% for role in work_experience %}
                <h3>{{ role.title }} — {{ role.organization }}</h3>
                <div class="meta">
                    {{ role.start_date }} – {{ role.end_date }}{% if role.location %} • {{ role.location }}{% endif %}
                </div>

                {% if role.summary %}<p>{{ role.summary }}</p>{% endif %}

                {% if role.responsibilities %}
                    <ul>
                        {% for item in role.responsibilities %}
                            <li>{{ item }}</li>
                        {% endfor %}
                    </ul>
                {% endif %}

                {% if role.technologies %}
                    <div class="tags">Tech: {{ role.technologies | join(", ") }}</div>
                {% endif %}
                {% if role.linked_projects %}
                    <div style="background: #f9f9f9; padding: 0.5rem; border-left: 3px solid #0056b3; margin: 0.5rem 0;">
                        <strong>Relevant Projects:</strong>
                        {% for p in role.linked_projects %}
                            <a href="{{ p.url }}">{{ p.name }}</a>{% if not loop.last %}, {% endif %}
                        {% endfor %}
                    </div>
                {% endif %}
            {% endfor %}
        </section>

        <section>
            <h2>Resumes</h2>
            <ul>
                {% for r in resumes %}
                    {% if r.status == "active" %}
                        <li><strong><a href="{{ r.url }}">{{ r.label }}</a></strong>{% if r.description %} —
                            {{ r.description }}{% endif %}</li>
                    {% endif %}
                {% endfor %}
            </ul>
        </section>
    {% endif %}


    {% if config.modes.current == "job_hunting" or config.modes.current == "project_promotion" %}
        <section>
            <h2>Selected Projects</h2>
            <table>
                <thead>
                <tr>
                    <th style="width: 25%">Project</th>
                    <th>Description</th>
                </tr>
                </thead>
                <tbody>
                {% for project in projects %}
                    {% if project.featured %}
                        <tr>
                            <td>
                                <strong><a href="{{ project.url }}">{{ project.name }}</a></strong>
                                <div class="tags">
                                    {{ project.tags|join(", ") }}
                                </div>
                            </td>
                            <td>
                                {{ project.description }}
                                {% if project.repository_url %}
                                    <div class="meta" style="margin-top:4px;">
                                        <a href="{{ project.repository_url }}">Source Code &rarr;</a>
                                    </div>
                                {% endif %}
                            </td>
                        </tr>
                    {% endif %}
                {% endfor %}
                </tbody>
            </table>
            <div style="text-align: right; margin-top: 0.5rem; font-size: 0.9rem;">
                <a href="projects.html">View Full Project List &rarr;</a>
            </div>
        </section>
    {% endif %}

    <section>
        <h2>Public Activity</h2>
        <div style="display: flex; gap: 2rem;">
            <div style="flex: 1;">
                <h3>Talks</h3>
                <ul>
                    {% for talk in identity.talks %}
                        <li><a href="{{ talk.url }}">{{ talk.title }}</a></li>
                    {% endfor %}
                </ul>
            </div>

            {% if config.modes.current == "job_hunting" and config.modes.job_hunting.resume_url %}
                <div style="flex: 1;">
                    <h3>Downloads</h3>
                    <ul>
                        <li><a href="{{ config.modes.job_hunting.resume_url }}"><strong>Download Full Resume
                            (PDF)</strong></a></li>
                    </ul>
                </div>
            {% endif %}
        </div>
    </section>

{% endblock %}
```
## File: src\github_is_my_cms\templates\professional\pages\projects.html.j2
```
{% extends "layouts/master.html.j2" %}

{% block body %}
    <section>
        <h2>Project Portfolio</h2>
        <p>A complete list of active projects, tools, and libraries.</p>

        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">Name</th>
                    <th style="width: 15%;">Status</th>
                    <th>Description</th>
                    <th style="width: 20%;">Tags</th>
                </tr>
            </thead>
            <tbody>
            {% for project in projects %}
                {% if not (project.cms and project.cms.suppress) %}
                <tr>
                    <td>
                        <a href="{{ project.url or project.repository_url }}"><strong>{{ project.name }}</strong></a>
                    </td>
                    <td>
                        <span style="font-size: 0.85rem; text-transform: capitalize;">{{ project.status }}</span>
                    </td>
                    <td>
                        {{ project.description }}
                        {% if project.repository_url %}
                         <a href="{{ project.repository_url }}" class="meta">[Repo]</a>
                        {% endif %}
                    </td>
                    <td>
                        <span class="tags">{{ project.tags|join(", ") }}</span>
                    </td>
                </tr>
                {% endif %}
            {% endfor %}
            </tbody>
        </table>
    </section>

    <section>
        <h2>PyPI Packages</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 20%;">Package</th>
                    <th style="width: 15%;">Version</th>
                    <th>Summary</th>
                    <th style="width: 15%; text-align: right;">Downloads/Mo</th>
                </tr>
            </thead>
            <tbody>
            {% for pkg in pypi %}
                <tr>
                    <td>
                        <a href="{{ pkg.docs_url or 'https://pypi.org/project/' ~ pkg.package_name }}">{{ pkg.package_name }}</a>
                    </td>
                    <td>{{ pkg.version }}</td>
                    <td>{{ pkg.summary }}</td>
                    <td style="text-align: right;">{{ pkg.downloads_monthly }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </section>
{% endblock %}
```
## File: src\github_is_my_cms\templates\professional\pages\projects.md.j2
```
{% extends "layouts/master.md.j2" %}

{% block body %}
## Curated Projects

| Project | Status | Description |
|:--------|:-------|:------------|
{% for project in projects %}
| [{{ project.name }}]({{ project.url }}) | {{ project.status }} | {{ project.description }} <br> <sub>Tags: {{ project.tags|join(", ") }}</sub> |
{% endfor %}

## PyPI Packages

| Package | Version | Downloads | Summary |
|:--------|:--------|:----------|:--------|
{% for pkg in pypi %}
| [{{ pkg.package_name }}]({{ pkg.docs_url or "https://pypi.org/project/" ~ pkg.package_name }}) | {{ pkg.version }} | {{ pkg.downloads_monthly }} | {{ pkg.summary }} |
{% endfor %}
{% endblock %}
```
## File: src\github_is_my_cms\templates\professional\pages\README.en.md.j2
```
{% extends "layouts/master.md.j2" %}
{# --- MACRO DEFINITIONS --- #}
{% macro section_skills() %}
## Skills
{{ identity.content.skills_intro }}

{# Render Headers #}
| {% for cat in identity.skills %}{{ cat.category }} | {% endfor +%}
| {% for cat in identity.skills %}-{{ "-" * cat.category|length }}- | {% endfor +%}
{# Render Transposed Rows #}
{% for row in identity.skill_rows -%}
| {% for cell in row %}{{ cell }}<br> | {% endfor +%}
{% endfor +%}
{% endmacro %}

{% macro section_resumes() %}
## Resumes
{% for r in resumes if r.status == "active" %}
{{ r.icon or "📄" }} [{{ r.label }}]({{ r.url }}){% if r.description %} {{ r.description }}{% endif %}<br>
{% endfor %}
{% endmacro %}

{% macro section_projects() %}
## Projects

{% if config.modes.current == "job_hunting" %}
{# --- MODE: JOB HUNTING (Simplified List) --- #}
*Selected highlights. For a complete portfolio, [view the full project list](projects.md).*

{% for project in projects %}
    {% if project.featured %}
* **[{{ project.name }}]({{ project.url or project.repository_url }})**
  <br>{{ project.description }}
  <br>_{{ project.tags | join(", ") }}_
    {% endif %}
{% endfor %}

{% else %}
{# --- MODE: PROJECT PROMOTION (Full Table) --- #}
| Project | Status | Description |
|:--------|:-------|:------------|
{% for project in projects %}
| [{{ project.name }}]({{ project.url or project.repository_url }}) | {{ project.status }} | {{ project.description }} <br> <sub>Tags: {{ project.tags|join(", ") }}</sub> |
{% endfor %}

{% endif %}
{% endmacro %}

{% macro section_experience() %}
## Work Experience
{% for role in work_experience %}
### {{ role.title }} @ {{ role.organization }}
{{ role.summary }}
{% if role.linked_projects %}
*Related Projects:* {% for p in role.linked_projects %}[{{ p.name }}]({{ p.url }}){% if not loop.last %}, {% endif %}{% endfor %}
{% endif %}
{% endfor %}
{% endmacro %}




{% block body %}
# {{ identity.name }}
{{ identity.tagline }}

{# --- LAYOUT LOGIC --- #}

{% if config.modes.current == "job_hunting" %}
    {{ section_skills() }}
    {{ section_resumes() }}
    {{ section_experience() }}
    {{ section_projects() }}
{% elif config.modes.current == "self_promotion" %}
    {{ section_skills() }}
    {{ section_talks() }}
    {{ section_projects() }}
{% else %}
    {# Default: Project Promotion #}
    {{ section_projects() }}
    {{ section_skills() }}
{% endif %}
{% endblock %}
```
## File: src\github_is_my_cms\templates\professional\pages\skill_detail.html.j2
```
{% extends "layouts/master.html.j2" %}

{% block body %}
<nav aria-label="breadcrumb">
  <ul>
      <li><a href="../index.html">Home</a></li>
      <li>Skills</li>
      <li>{{ skill_name }}</li>
  </ul>
</nav>

<h1>Projects using {{ skill_name }}</h1>

<div class="project-grid">
    {% for project in skill_projects %}
    <article>
        <header>
            <strong><a href="{{ project.url or project.repository_url }}">{{ project.name }}</a></strong>
        </header>
        <p>{{ project.description }}</p>
        <footer>
            <small>
                {% for tag in project.tags %}
                    {% if tag|lower == skill_name|lower %}
                        <strong>#{{ tag }}</strong>
                    {% else %}
                        #{{ tag }}
                    {% endif %}
                {% endfor %}
            </small>
        </footer>
    </article>
    {% endfor %}
</div>

<p style="margin-top: 2rem;">
    <a href="../index.html">&larr; Back to Resume</a>
</p>
{% endblock %}
```
```
## File: data_sample\identity.toml
```
# src/github_is_my_cms/data/identity.toml

name = "Matthew Dean Martin"
tagline = "Pythonist, Devops Guy, and Govtech Specialist"
location = "United States"
pypi_username = "matthewdeanmartin"
github_username =  "matthewdeanmartin"

[content]
skills_intro = "I used to be a full stack developer, I evolved into tech lead and most recently devops work. I write code and know how to ship in a govtech environment."
projects_intro = "Here is a collection of my manual projects and published PyPI packages."
job_hunting_intro = "I am currently looking for new opportunities. My focus is on production-quality backend systems."

# --- Resumes ---
[[resumes]]
label = "Resume from 2015"
url = "https://matthewdeanmartin.github.io/"
icon = "📄"

[[resumes]]
label = "Novelty Resume from 2024"
url = "https://matthewdeanmartin.github.io/resume/browser/"
description = "Hire button and a fire button!"
icon = "📄"

# --- Talks ---
[[talks]]
title = "Python Librarian"
url = "https://www.youtube.com/channel/UCw1p2a3LW1VG7DTZQaT8Oaw"
icon = "▶️"

# --- Skills ---
# Column 1
[[skills]]
category = "Devops"
[[skills.skills]]
name = "Typescript for AWS CDK"
level = "Expert"
icon = "🌐"
[[skills.skills]]
name = "Terraform for AWS / HCL"
level = "Expert"
icon = "🪐"
[[skills.skills]]
name = "Go for Terratest"
level = "Good enough"
icon = "🐹"

# Column 2
[[skills]]
category = "Backend Development"
[[skills.skills]]
name = "Python for Serverless in AWS"
level = "Expert"
icon = "🐍"
[[skills.skills]]
name = "Postgres"
icon = "🐘"
[[skills.skills]]
name = "DynamoDB"
icon = "🗄️"

# Column 3
[[skills]]
category = "Build Master"
[[skills.skills]]
name = "Gitlab Pipelines"
level = "Expert"
icon = "🦊"
[[skills.skills]]
name = "Bash for Gitlab"
level = "Very Good"
icon = "`>_`"

# --- Profiles (Backlinks) ---

# Group: Social Media with Backlinks
[[profiles]]
service = "Mastodon"
handle = "mastodon.social/@mistersql"
url = "https://mastodon.social/@mistersql"
group = "social"
icon = "🐘"

[[profiles]]
service = "BlueSky"
handle = "bsky.app"
url = "https://bsky.app/profile/mistersql.bsky.social"
group = "social"
icon = "🦋"

[[profiles]]
service = "LinkedIn"
handle = "LinkedIn"
url = "https://linkedin.com/in/matthewdeanmartin"
group = "social"
icon = "🔗"


# Group: Verified Profile Pages
[[profiles]]
service = "Dev.to"
handle = "dev.to"
url = "https://dev.to/matthewdeanmartin"
group = "verified"
icon = "💻"

[[profiles]]
service = "Gravatar"
handle = "Gravatar"
url = "https://gravatar.com/matthewdmartin"
group = "verified"
icon = "🌀"

[[profiles]]
service = "StackOverflow"
handle = "StackOverflow"
url = "https://stackoverflow.com/users/33264/matthewmartin"
group = "verified"
icon = "🔥"
```
## File: data_sample\projects.toml
```
# src/github_is_my_cms/data/projects.toml

[[projects]]
slug = "Hicmah"
name = "Hicmah"
description = "Hicmah - Hit Counter Module and Handler"
url = "https://github.com/matthewdeanmartin/Hicmah"
repository_url = "https://github.com/matthewdeanmartin/Hicmah"
tags = [
    "analytics",
    "handler",
    "hit-counter",
    "javascript",
    "module",
    "web-development",
]
status = "active"
related_skills = ["AWS", "Serverless"]

[projects.cms]
suppress = false
package_links = []
```
## File: data_sample\pypi_projects.toml
```
# src/github_is_my_cms/data/pypi_projects.toml

[[packages]]
package_name = "dedlin"
github_repo = "matthewdeanmartin/dedlin"
version = "1.0.0"
summary = "A modern python port of the classic edlin line editor."
downloads_monthly = 543
docs_url = "https://dedlin.readthedocs.io"
last_updated = "2024-11-20"

[[packages]]
package_name = "cli_tool_audit"
github_repo = "matthewdeanmartin/cli_tool_audit"
version = "0.4.2"
summary = "Audit your CLI tools for version and existence."
downloads_monthly = 1200
last_updated = "2024-10-15"
```
## File: data_sample\readme_cms.toml
```
# src/github_is_my_cms/data/readme_cms.toml
theme = "professional"

[mode]
# Options: "job_hunting", "project_promotion", "self_promotion"
current = "project_promotion"

[mode.job_hunting]
enable_projects = true
project_visibility = "curated"
resume_url = "https://matthewdeanmartin.github.io/matthewdeanmartin"

[mode.project_promotion]
enable_projects = true
project_visibility = "full"
highlight_pypi = true

[mode.self_promotion]
enable_talks = true
enable_posts = true
highlight_blog = true

[languages]
default = "en"
supported = ["en"]
```
## File: data_sample\resumes.toml
```
# data/resumes.toml

[[resumes]]
id = "resume-2015"
label = "Resume from 2015"
url = "https://matthewdeanmartin.github.io/"
format = "html"          # pdf | docx | html | md | other
audience = "general"
status = "expired"       # active | expired | draft
valid_from = "2015-01"
icon = "📄"

[[resumes]]
id = "resume-2024-novelty"
label = "Novelty Resume from 2024"
url = "https://matthewdeanmartin.github.io/resume/browser/"
format = "html"
audience = "general"
status = "active"
valid_from = "2024-01"
description = "Hire button and a fire button!"
icon = "📄"
```
## File: data_sample\work_experience.toml
```
# data/work_experience.toml

[[experience]]
id = "acme-2021-2024"
organization = "Acme Corp"
title = "Senior Platform Engineer"
employment_type = "full_time" # full_time | contract | freelance | volunteer
start_date = "2021-06"
end_date = "2024-11"         # or "present"
location = "Remote"
summary = "Owned CI/CD, platform observability, and infra automation for regulated workloads."

responsibilities = [
  "Built multi-account AWS landing zone with policy-as-code.",
  "Reduced deploy time from 40m to 10m via pipeline refactors.",
]

technologies = ["AWS", "Terraform", "Python", "Postgres"]
links = [
  { label = "Company", url = "https://example.com" }
]

related_project_slugs = ["Hicmah", "dedlin"]
```
## File: src\GHIP_001_Specification.md
```markdown
# GHIP-000 — github-is-my-cms (v2)

Title: github-is-my-cms, a GitHub-centric personal site and profile CMS
Author: Matthew Dean Martin
Status: Draft
Type: Standards Track
Version: 2.0
Created: 2025-12-14
Supersedes: GHIP-001

______________________________________________________________________

## Abstract

GHIP-000 (v2) defines a Python-based content management system for GitHub profile repositories that compiles structured data and authored Markdown into Markdown, HTML, and a navigable static JSON API described by OpenAPI.

This revision formalizes the system as it has evolved beyond GHIP-001, most notably:

- A **resource-oriented static API** with pagination, relationships, and HATEOAS-style linking.
- **First-class work experience and resume artifacts**, designed explicitly for job-hunting use cases.
- A **theme contract** that allows interchangeable presentation layers without changing data or content.
- Clear separation between **user-owned repository data** and the **CMS engine package**.

Internationalization, translation automation, and linting remain defined but optional and may be implemented incrementally.

______________________________________________________________________

## Motivation

GitHub profile READMEs have evolved from single static documents into living representations of a developer’s professional identity. GHIP-001 demonstrated that this could be systematized, but the initial specification underestimated several realities:

- Static APIs are more useful when they are **navigable**, not monolithic blobs.
- Job-hunting requires **structured work history and resume artifacts**, not just projects.
- Theming is unavoidable once Markdown and HTML are treated as parallel first-class outputs.
- Data ownership must clearly belong to the repository, not the CMS engine.

GHIP-000 updates the specification to match the working implementation and to explicitly prioritize professional work history and resumes as primary data types.

______________________________________________________________________

## Goals and Non-Goals

### Goals

1. **Markdown-first authoring, multi-format output**

   - Markdown is the canonical authored format.
   - HTML and JSON are compiled artifacts.

1. **Navigable Static API**

   - Resource-oriented endpoints.
   - Pagination for large collections.
   - Stable relationships between resources (projects, PyPI packages, work experience, resumes).

1. **Job-hunting as a first-class mode**

   - Work experience modeled explicitly.
   - Resume files treated as versioned, role-specific artifacts.

1. **Themeable presentation layer**

   - Multiple themes can render the same data.
   - Themes may add or omit pages, but must follow a defined contract.

1. **Repository-owned data**

   - All user data lives in the repository.
   - The CMS package contains no user-specific content.

### Non-Goals

- Not a general-purpose CMS.
- Not a dynamic backend service.
- Not a real-time API.
- Not a full resume builder or ATS replacement.

______________________________________________________________________

## Repository Layout (v2)

```text
.github/
    workflows/
        readme_cms.yml        # Optional automation

data/
    identity.toml             # Core identity and skills
    projects.toml             # GitHub and manual projects
    pypi_projects.toml        # PyPI packages
    work_experience.toml      # Employment and contract history
    resumes.toml              # Resume artifacts and metadata

src/
    content/                  # Authored Markdown content
        pages/
        projects/
        experience/

    github_is_my_cms/          # CMS engine (Python package)
        builder.py
        cli.py
        config.py
        models.py
        data_sources.py
        templates/


docs/
    md/                        # Generated Markdown pages
    apis/                      # Static JSON API + OpenAPI
    index.html                 # GitHub Pages entrypoint

README.md                     # Root profile README
readme_cms.toml               # CMS configuration
```

______________________________________________________________________

## Modes

The CMS supports multiple operational modes. Modes primarily affect **content emphasis**, not data availability.

### Defined Modes

- `job_hunting`
- `project_promotion`
- `self_promotion`

Modes:

- Do **not** change the underlying data model.
- May affect which sections are rendered and which pages are linked prominently.
- Are applied at render time, not data load time.

______________________________________________________________________

## Core Data Models

### Identity

Identity represents stable personal and professional attributes.

Includes:

- Name, tagline, location
- Skills (grouped, structured)
- Social and verified profiles
- Talks and public appearances

Twitter/X identities are explicitly forbidden.

______________________________________________________________________

### Projects

Projects represent discrete technical works, typically backed by GitHub repositories.

Sources:

- Manually curated entries
- GitHub-synced metadata

Projects may relate to:

- PyPI packages
- Work experience entries (optional)

______________________________________________________________________

### PyPI Packages

PyPI packages represent published Python artifacts.

Characteristics:

- Fetched and refreshed automatically
- May map to one or more GitHub projects
- Treated as read-only derived data

Future versions may incorporate richer metadata sources (e.g. download statistics, release cadence).

______________________________________________________________________

## Work Experience (First-Class)

Work experience is a primary data type in GHIP-000.

Each entry represents a role, not a project.

### Work Experience Fields

A work experience entry includes:

- Organization name
- Role / title
- Employment type (full-time, contract, freelance, volunteer)
- Start date
- End date (or `present`)
- Location (remote / onsite / hybrid)
- Summary
- Responsibilities (bullet list)
- Technologies used
- Optional links (company site, product, press)

Work experience entries:

- Are rendered prominently in job-hunting mode.
- May be summarized or omitted in other modes.
- Are exposed via the static API as a paginated collection.

______________________________________________________________________

## Resumes (Artifact-Oriented)

Resumes are treated as **artifacts**, not text blobs.

A resume represents a concrete file intended for distribution.

### Resume Metadata

Each resume entry includes:

- Label (human-readable name)
- File URL (PDF, DOCX, HTML, etc.)
- Format
- Intended role or audience
- Status (`active`, `expired`, `draft`)
- Valid-from and optional valid-until dates
- Optional description

Resumes:

- Are surfaced prominently in job-hunting mode.
- May be hidden or de-emphasized in other modes.
- Are exposed as a first-class API resource.

______________________________________________________________________

## Static API (v2)

The CMS generates a static, navigable JSON API under `docs/apis/`.

### API Characteristics

- Read-only
- File-backed
- Hypermedia-inspired (links and refs)

### Resource Types

- Identity
- Configuration
- Projects
- PyPI Packages
- Work Experience
- Resumes

### Collections

Collections are exposed as:

- `/index.json` (full index, refs only)
- `/pages/{n}.json` (paged refs)
- `/by-id/{id}.json` (full resource)

Resources include:

- `_links` for navigation
- `_rels` for relationships to other resources

______________________________________________________________________

## OpenAPI

An OpenAPI specification is generated alongside the static API.

The OpenAPI document:

- Describes the **actual emitted payloads**, including refs and links.
- Is intended for documentation, client generation, and exploration.
- Is rendered via Swagger UI under GitHub Pages.

______________________________________________________________________

## Themes

Themes define presentation, not data.

### Theme Contract

A theme:

- Is a directory under `templates/`.

- May include Markdown and HTML templates.

- Must support a minimal required set of templates:

  - Root index page
  - Projects listing
  - API/Swagger link

Themes:

- May add additional pages.
- Must not assume undocumented data fields.
- Should render sensibly in both Markdown and HTML.

______________________________________________________________________

## Internationalization

Internationalization is supported but optional.

Current state:

- Single-language builds are fully supported.
- Language configuration is defined but translation automation is not mandatory.

Future implementations may add:

- LLM-based translation
- Source-hash tracking
- Per-language navigation

______________________________________________________________________

## Linting and Validation

Linting is intentionally minimal in v2.

Guaranteed validations:

- Schema validation via Pydantic models
- Forbidden identity enforcement (e.g. Twitter/X)

Additional linting (links, content structure, output integrity) may be added incrementally.

______________________________________________________________________

## Backwards Compatibility

GHIP-000 supersedes GHIP-001.

No backwards compatibility is guaranteed. Existing repositories may migrate by:

1. Moving data into the `data/` directory.
1. Adding work experience and resume metadata.
1. Regenerating outputs with the v2 CMS.

______________________________________________________________________

## Security and Privacy Considerations

- All data is static and publicly visible once published.
- Users must explicitly choose which identities and resumes are exposed.
- API tokens are used only during data refresh and are never committed.

______________________________________________________________________

End of GHIP-000 (v2)
```
## File: src\github_is_my_cms\builder.py
```python
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
```
## File: src\github_is_my_cms\builder_api.py
```python
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
```
## File: src\github_is_my_cms\cli.py
```python
# src/github_is_my_cms/cli.py
"""
Command-line interface for the github-is-my-cms.
Handles argument parsing, logging setup, and command dispatch.
"""

import argparse
import logging
import logging.config
import sys
from pathlib import Path
from typing import List, Optional

import github_is_my_cms.__about__ as __about__
from github_is_my_cms.builder_api import SiteBuilderAPI
from github_is_my_cms.logging_config import generate_config

# Import the builder
from .builder import SiteBuilder
from .data_sources import DataUpdater

# Versioning
# TODO: ideally fetched from package metadata in production
VERSION = __about__.__version__

logger = logging.getLogger(__name__)


def setup_logging(level_name: str):
    """
    Configures the root logger based on the user's verbosity selection.
    """
    numeric_level = getattr(logging, level_name.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level_name}")
    print(level_name)
    logging.config.dictConfig(generate_config(level=level_name))
    logger.debug("Testing 1123")
    # logging.basicConfig(
    #     level=numeric_level,
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #     datefmt="%H:%M:%S",
    # )


def cmd_build(args: argparse.Namespace):
    """
    Handler for the 'build' subcommand.
    Compiles Markdown and HTML pages.
    """
    logging.info("Starting build process...")
    try:
        builder = SiteBuilder(root_dir=args.root)
        api_builder = SiteBuilderAPI(root_dir=args.root)
        builder.clean()
        api_builder.build_static_api()
        builder.build_markdown_pages()
        builder.build_html_pages()
        logging.info("Build completed successfully.")
    except Exception as e:
        logging.error(f"Build failed: {e}", exc_info=True)
        sys.exit(1)


def cmd_lint(args: argparse.Namespace):
    """
    Placeholder: Validates content structure, links, and TOML data.
    """
    logging.warning("Command 'lint' is not yet implemented.")
    logging.info(f"Would scan root: {args.root}")
    # TODO: Implement quality checks defined in GHIP-001 "Quality Checks"


def cmd_translate(args: argparse.Namespace):
    """
    Placeholder: Runs LLM-based translation for non-default languages.
    """
    logging.warning("Command 'translate' is not yet implemented.")
    # TODO: Implement LLM integration defined in GHIP-001 "Translation Workflow"


def cmd_update_data(args: argparse.Namespace):
    """
    Fetches fresh data from PyPI and updates the local TOML files.
    """
    logging.info("Starting data update...")

    if DataUpdater is None:
        logging.error("DataUpdater module not found.")
        sys.exit(1)

    root_path = Path(args.root)
    updater = DataUpdater(root_dir=root_path)

    try:
        # 1. Update GitHub Projects (Source of Truth)
        updater.update_projects_from_github()

        # 2. Update PyPI Metadata (Supplementary)
        updater.update_pypi_data()
        logging.info("Data update completed.")
    except Exception as e:
        logging.error(f"Update failed: {e}", exc_info=True)
        sys.exit(1)


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="github-is-my-cms, a github centric profile and readme generator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # --- Global Arguments ---
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        "--log-level",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging verbosity.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Path to the repository root containing readme_cms.toml.",
    )

    # --- Subcommands ---
    subparsers = parser.add_subparsers(
        title="Commands", dest="command", help="Available operations"
    )

    # Command: build
    parser_build = subparsers.add_parser(
        "build", help="Compile TOML and Markdown into final docs/ artefacts."
    )
    parser_build.set_defaults(func=cmd_build)

    # Command: lint (Placeholder)
    parser_lint = subparsers.add_parser(
        "lint", help="Validate links, content structure, and data integrity."
    )
    parser_lint.set_defaults(func=cmd_lint)

    # Command: translate (Placeholder)
    parser_translate = subparsers.add_parser(
        "translate", help="Regenerate translations using configured LLM provider."
    )
    parser_translate.set_defaults(func=cmd_translate)

    # Command: update-data (Placeholder)
    parser_update = subparsers.add_parser(
        "update-data", help="Refresh cached data from PyPI and GitHub APIs."
    )
    parser_update.set_defaults(func=cmd_update_data)

    # --- Execution Logic ---

    # Check for empty args (excluding script name) to default to help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(argv)

    # Apply logging configuration
    setup_logging(args.log_level)

    # Dispatch to function
    if hasattr(args, "func"):
        args.func(args)
    else:
        # Fallback if valid command structure but no func mapped (unlikely with subparsers)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
```
## File: src\github_is_my_cms\config.py
```python
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
```
## File: src\github_is_my_cms\data_sources.py
```python
"""
data_sources.py
Handles fetching external data from PyPI and GitHub APIs to update local TOML caches.
"""

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

import httpx
import tomli_w
from bs4 import BeautifulSoup

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

    BASE_URL = "https://pypi.org/user"

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
                    logger.info(
                        f"PyPI: Using cached package list for user '{username}'."
                    )
                    return data.get("packages", [])
            except json.JSONDecodeError:
                pass

        # 2. Fetch via HTTPX + BS4
        logger.info(
            f"PyPI: Discovering packages for user '{username}' via HTML scraping..."
        )

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
                package_names = sorted(
                    list(set(s.get_text(strip=True) for s in snippets))
                )

            # 3. Save Cache
            cache_payload = {
                "user": username,
                "timestamp": datetime.now().isoformat(),
                "packages": package_names,
            }
            self.cache_file.write_text(
                json.dumps(cache_payload, indent=2), encoding="utf-8"
            )

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
            req = urllib.request.Request(
                url, headers={"User-Agent": "github-is-my-cms/0.1.0"}
            )
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
                    "github_repo": self._extract_github_repo(
                        info.get("project_urls") or {}
                    ),
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
            logger.warning(
                "Could not load full config; some auto-discovery features may fail."
            )
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
        pkg_map = {
            p["package_name"]: p for p in existing_packages if "package_name" in p
        }

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
            logger.info(
                "No pypi_username configured in identity.toml. Skipping auto-discovery."
            )

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

        logger.info(
            f"Successfully updated {self.pypi_file} with {len(updated_list)} packages."
        )
```
## File: src\github_is_my_cms\models.py
```python
"""
models.py
Data structures for the github-is-my-cms.
Implements schema validation and JSON serialization for the Static API.
"""

from __future__ import annotations

import itertools
import logging
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

logger = logging.getLogger(__name__)
# --- Enums ---


class SiteMode(str, Enum):
    """The three operational modes defined in GHIP-001."""

    JOB_HUNTING = "job_hunting"
    PROJECT_PROMOTION = "project_promotion"
    SELF_PROMOTION = "self_promotion"


class ProjectVisibility(str, Enum):
    """Controls how much detail is shown for projects in different modes."""

    CURATED = "curated"
    MINIMAL = "minimal"
    FULL = "full"


# --- New Models for Skills & Resumes ---


class Skill(BaseModel):
    name: str
    level: Optional[str] = None  # e.g. "Expert", "Very Good"
    icon: Optional[str] = None  # e.g. "🌐", "🐍"

    def display(self) -> str:
        parts = []
        if self.icon:
            parts.append(self.icon)
        parts.append(self.name)
        if self.level:
            parts.append(f"- {self.level}")
        return " ".join(parts)


class SkillGroup(BaseModel):
    category: str  # Header, e.g. "Devops"
    skills: List[Skill] = []


class ResumeEntry(BaseModel):
    label: str  # "Resume from 2015"
    url: HttpUrl
    description: Optional[str] = None  # "Hire button and a fire button!"
    icon: str = "📄"


class TalkEntry(BaseModel):
    title: str
    url: HttpUrl
    icon: str = "▶️"


# --- Identity Models ---


class SocialProfile(BaseModel):
    """
    Represents a node in the Identity Graph.
    """

    service: str = Field(
        ..., description="Name of the service (e.g., github, linkedin)"
    )
    handle: str = Field(..., description="Username or handle")
    url: HttpUrl = Field(..., description="Link to the profile")
    group: str = Field("social", description="Group key: 'social' or 'verified'")
    same_as: List[HttpUrl] = Field(
        default_factory=list, description="List of equivalent URLs for JSON-LD"
    )
    icon: Optional[str] = None  # e.g. "🌐", "🐍"

    @field_validator("url", "service")
    @classmethod
    def validate_no_twitter(cls, v: Any, info) -> Any:
        """
        GHIP-001 Quality Check: Strictly forbid Twitter/X.
        """
        forbidden = ["twitter.com", "x.com"]
        val_str = str(v).lower()
        if any(f in val_str for f in forbidden):
            raise ValueError(f"Twitter/X links are strictly forbidden by GHIP-001: {v}")
        return v


class IdentityContent(BaseModel):
    skills_intro: Optional[str] = None
    projects_intro: Optional[str] = None
    job_hunting_intro: Optional[str] = None


class Identity(BaseModel):
    """
    Core personal information and aggregation of the identity graph.
    """

    name: str
    tagline: str
    location: Optional[str] = None
    email: Optional[str] = None

    pypi_username: Optional[str] = Field(
        None, description="Username on PyPI to auto-discover packages"
    )
    github_username: Optional[str] = Field(
        None, description="Username on GitHub to filter repos"
    )

    profiles: List[SocialProfile] = Field(
        default_factory=list, description="The Identity Graph"
    )

    resumes: List[ResumeEntry] = Field(default_factory=list)
    skills: List[SkillGroup] = Field(default_factory=list)
    talks: List[TalkEntry] = Field(default_factory=list)

    content: IdentityContent = Field(default_factory=IdentityContent)

    @property
    def skill_rows(self) -> List[List[str]]:
        """
        Helper to transpose columns (Categories) into Markdown Table Rows.
        Returns a list of rows, where each row is a list of strings (cells).
        """
        if not self.skills:
            return []

        # Get list of skill-lists: [[s1, s2], [s3, s4], [s5]]
        columns = [group.skills for group in self.skills]
        # zip_longest fills missing items with None
        rows = itertools.zip_longest(*columns, fillvalue=None)

        rendered_rows = []
        for row in rows:
            # Render each cell
            rendered_row = []
            for item in row:
                if item:
                    rendered_row.append(item.display())
                else:
                    rendered_row.append("")
            rendered_rows.append(rendered_row)
        return rendered_rows


# --- Project Models ---


class CMSDirective(BaseModel):
    suppress: bool = False
    package_links: List[HttpUrl] = []


class Project(BaseModel):
    """
    A manually curated project entry (from projects.toml).
    """

    slug: str = Field(..., description="Unique identifier for the project")
    name: str
    description: str
    url: Optional[HttpUrl] = None
    repository_url: Optional[HttpUrl] = None
    tags: List[str] = Field(default_factory=list)
    featured: bool = False
    status: str = Field("active", description="active, archived, or maintenance")

    cms: Optional[CMSDirective] = None

    related_skills: List[str] = Field(default_factory=list)


class SkillPageContext(BaseModel):
    skill: Skill
    projects: List[Project]
    slug: str


class PyPIPackage(BaseModel):
    """
    Auto-generated metadata from PyPI (from pypi_projects.toml).
    """

    package_name: str
    github_repo: Optional[str] = Field(None, description="owner/repo format")
    version: Optional[str] = None
    summary: Optional[str] = None
    downloads_monthly: Optional[int] = 0
    docs_url: Optional[HttpUrl] = None
    last_updated: Optional[str] = None


# --- Configuration & Mode Models ---


class JobHuntingSettings(BaseModel):
    enable_projects: bool = True
    project_visibility: ProjectVisibility = ProjectVisibility.CURATED
    highlight_skills: bool = True
    resume_url: Optional[HttpUrl] = None


class ProjectPromotionSettings(BaseModel):
    enable_projects: bool = True
    project_visibility: ProjectVisibility = ProjectVisibility.FULL
    highlight_pypi: bool = True


class SelfPromotionSettings(BaseModel):
    enable_talks: bool = True
    enable_posts: bool = True
    highlight_blog: bool = True


class ModeConfig(BaseModel):
    """
    Configuration container for mode-specific behaviors.
    """

    current: SiteMode = SiteMode.PROJECT_PROMOTION
    job_hunting: JobHuntingSettings = Field(default_factory=JobHuntingSettings)
    project_promotion: ProjectPromotionSettings = Field(
        default_factory=ProjectPromotionSettings
    )
    self_promotion: SelfPromotionSettings = Field(default_factory=SelfPromotionSettings)


class LanguageConfig(BaseModel):
    default: str = "en"
    supported: List[str] = ["en"]


# --- Root CMS Model ---


class CMSConfig(BaseModel):
    """
    The aggregate model representing the entire state of the CMS.
    This maps to the logical structure of the TOML files combined.
    """

    identity: Identity
    modes: ModeConfig = Field(default_factory=ModeConfig)
    languages: LanguageConfig = Field(default_factory=LanguageConfig)
    projects: List[Project] = Field(default_factory=list)
    pypi_packages: List[PyPIPackage] = Field(default_factory=list)
    theme: Optional[str] = "default"

    work_experience: List[WorkExperienceEntry] = Field(default_factory=list)
    resumes: List[ResumeArtifact] = Field(default_factory=list)

    @property
    def featured_resume_url(self) -> Optional[str]:
        for r in self.resumes:
            if r.status == ResumeStatus.ACTIVE:
                return str(r.url)
        return None

    @property
    def current_mode_settings(self):
        """Helper to retrieve settings for the currently active mode."""
        if self.modes.current == SiteMode.JOB_HUNTING:
            return self.modes.job_hunting
        elif self.modes.current == SiteMode.PROJECT_PROMOTION:
            return self.modes.project_promotion
        elif self.modes.current == SiteMode.SELF_PROMOTION:
            return self.modes.self_promotion
        return self.modes.project_promotion


# --- add near other enums ---


class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    VOLUNTEER = "volunteer"


class ResumeStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    DRAFT = "draft"


class ResumeFormat(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"
    MD = "md"
    OTHER = "other"


class LabeledLink(BaseModel):
    label: str
    url: HttpUrl


class WorkExperienceEntry(BaseModel):
    id: str
    organization: str
    title: str
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    start_date: str  # "YYYY-MM" or "YYYY"
    end_date: str  # "YYYY-MM" or "present"
    location: Optional[str] = None
    summary: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)
    links: List[LabeledLink] = Field(default_factory=list)

    related_project_slugs: List[str] = Field(default_factory=list)
    # We will inject the actual Project objects here during the build step
    linked_projects: List[Project] = Field(default_factory=list, exclude=True)


class ResumeArtifact(BaseModel):
    id: str
    label: str
    url: HttpUrl
    format: ResumeFormat = ResumeFormat.PDF
    audience: Optional[str] = None
    status: ResumeStatus = ResumeStatus.ACTIVE
    valid_from: Optional[str] = None  # "YYYY-MM" or "YYYY"
    valid_until: Optional[str] = None  # optional
    description: Optional[str] = None
    icon: Optional[str] = "📄"
```
## File: .github\workflows\deploy.yml
```yaml
name: Deploy Static Content to Pages

on:
  # Runs on pushes targeting the default branch
  push:
    branches: ["master"]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# Sets permissions of the GITHUB_TOKEN to allow deployment to GitHub Pages
permissions:
  contents: read
  pages: write
  id-token: write

# Allow only one concurrent deployment
concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  # Single deploy job since we are just deploying existing files
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          # We upload the 'docs' directory as the site root
          path: './docs'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```
