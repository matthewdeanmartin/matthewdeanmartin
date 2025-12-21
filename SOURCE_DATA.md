## Tree for

```
├── AGENT.md
├── data_sample/
│   ├── identity.toml
│   ├── projects.toml
│   ├── pypi_projects.toml
│   ├── readme_cms.toml
│   ├── resumes.toml
│   ├── skills.toml
│   └── work_experience.toml
├── docs_app/
│   └── er.mermaid
├── readme_cms.toml
└── src/
    └── github_is_my_cms/
        ├── audit_links.py
        ├── builder.py
        ├── cli.py
        ├── config.py
        ├── data_sources.py
        ├── generate_skills.py
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

## File: data_sample\\identity.toml

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

## File: data_sample\\projects.toml

```
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
primary_language = "N/A"

[projects.cms]
suppress = false
package_links = []

[[projects]]
slug = "ai_fish_tank"
name = "ai_fish_tank"
description = "Fish tank that has a story going on"
url = "https://github.com/matthewdeanmartin/ai_fish_tank"
tags = [
    "aquarium",
    "artificial-intelligence",
    "game",
    "interactive-fiction",
    "python",
    "simulation",
    "storytelling",
]
status = "active"
repository_url = "https://github.com/matthewdeanmartin/ai_fish_tank"
primary_language = "Python"
```

## File: data_sample\\pypi_projects.toml

```
[[packages]]
package_name = "ai-shell"
downloads_monthly = 0
version = "1.0.4"
summary = "Filesystem Shell interface that an OpenAI Assitant can use as a tool."
docs_url = "https://github.com/matthewdeanmartin/ai_shell"
last_updated = "2025-12-20"
github_repo = "matthewdeanmartin/ai_shell"
tags = [
    "openai",
    "chatgpt",
]

[[packages]]
package_name = "bash2gitlab"
downloads_monthly = 0
version = "0.9.9"
summary = "Compile bash to gitlab pipeline yaml"
docs_url = "https://pypi.org/project/bash2gitlab/"
last_updated = "2025-12-20"
github_repo = "matthewdeanmartin/bash2gitlab"
tags = [
    "bash",
    "gitlab",
]

[[packages]]
package_name = "bitrab"
downloads_monthly = 0
version = "0.1.0"
summary = "Compile bash to gitlab pipeline yaml"
docs_url = "https://pypi.org/project/bitrab/"
last_updated = "2025-12-20"
github_repo = "matthewdeanmartin/bitrab"
tags = [
    "bash",
    "gitlab",
]
```

## File: data_sample\\readme_cms.toml

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

## File: data_sample\\resumes.toml

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

## File: data_sample\\skills.toml

```
[[skills]]
category = "Devops"

[[skills.skills]]
name = "Typescript for AWS CDK"
featured = true
level = "Expert"
icon = "🌐"
aliases = [
    "typescript",
    "angular",
]

[[skills.skills]]
name = "Terraform for AWS / HCL"
featured = true
level = "Expert"
icon = "🪐"
aliases = [
    "terraform",
    "hcl",
]


[[skills]]
category = "Inbox - From Resume"
skills = [
    { name = "VBA", level = "Competent", featured = true, aliases = [] },
    { name = "XML", level = "Competent", featured = true, aliases = [] },
]

[[skills]]
category = "Inbox - From GitHub"
skills = [
    { name = "Rust", level = "Competent", featured = true, icon = "💻", aliases = [] },
]
```

## File: data_sample\\work_experience.toml

```
# data/work_experience.toml

[[experience]]
id = "artemis-aretum-2019-present"
organization = "Artemis Consulting (renamed Aretum)"
title = "Technical Lead and Python Developer"
employment_type = "full_time"
start_date = "2019-09"
end_date = "present"
summary = "Technical lead for a Python-based search engine for legal documents at the Library of Congress (USCO)."

responsibilities = [
  "Application development: built three Python microservices, two ETL processes, and several AWS Lambdas for search, emailing, and bookmarking.",
  "Architecture and infrastructure-as-code: selected AWS services and wrote Terraform to integrate them with the application.",
  "Technical leadership: supported a specialist team on a cloud-native application; helped teammates with IDE/tooling and build scripts; set up Dev Containers; used LocalStack and Python moto for AWS simulation.",
  "Process: participated in SAFe-style Agile (PI planning, sprint planning, ticket writing, sprint demos) continuously for ~5 years; gathered metrics and helped client interpret them for continuous improvement.",
  "Release management: participated in Federal SDLC (A&A, ATO, POA&M responses, change requests for production releases).",
  "Supervision: participated in technical interviewing, developer onboarding, mentoring, and PIPs.",
]

technologies = [
  "Python",
  "pytest",
  "Connexion",
  "Gunicorn",
  "OpenAPI/Swagger",
  "JSON",
  "Nginx",
  "AWS ECS",
  "AWS ECR",
  "AWS S3",
  "AWS Glue",
  "AWS RDS",
  "AWS EC2",
  "AWS ALB",
  "AWS API Gateway",
  "AWS ElastiCache",
  "OpenSearch/Elasticsearch",
  "Terraform",
  "Docker",
  "Podman",
  "GitLab CI",
  "SonarQube",
  "pylint",
  "Locust",
  "mypy",
  "Makefile",
  "Justfile",
  "Git",
  "bash",
  "Java TestNG",
  "Selenium",
  "Angular",
  "Trivy",
  "OWASP ZAP",
  "Tenable",
  "Keycloak",
  "JWT",
  "VSCode",
  "WebStorm",
  "IntelliJ",
  "PyCharm",
]

links = []
```

## File: docs_app\\er.mermaid

```
erDiagram
    SITE_CONFIG ||--|| MODE_SELECTOR : selects
    SITE_CONFIG ||--|| LANGUAGE_CONFIG : defines
    MODE_SELECTOR ||--o| MODE_JOB_HUNTING : job_hunting
    MODE_SELECTOR ||--o| MODE_PROJECT_PROMOTION : project_promotion
    MODE_SELECTOR ||--o| MODE_SELF_PROMOTION : self_promotion

    IDENTITY ||--|| IDENTITY_CONTENT : has
    IDENTITY ||--o{ IDENTITY_RESUME_REF : references
    IDENTITY ||--o{ TALK : has
    IDENTITY ||--o{ SKILL_CATEGORY : has
    SKILL_CATEGORY ||--o{ SKILL : contains
    IDENTITY ||--o{ PROFILE : has

    RESUME ||--o{ IDENTITY_RESUME_REF : used_by

    PROJECT ||--o| PROJECT_CMS : has
    PROJECT ||--o{ PROJECT_TAG : has
    TAG ||--o{ PROJECT_TAG : labels

    PYPI_PACKAGE ||--o{ PACKAGE_TAG : has
    TAG ||--o{ PACKAGE_TAG : labels

    WORK_EXPERIENCE ||--o{ EXPERIENCE_RESPONSIBILITY : includes
    WORK_EXPERIENCE ||--o{ EXPERIENCE_TECHNOLOGY : uses
    WORK_EXPERIENCE ||--o{ EXPERIENCE_LINK : links

    SITE_CONFIG {
      string theme
    }

    MODE_SELECTOR {
      string current   "job_hunting|project_promotion|self_promotion"
    }

    MODE_JOB_HUNTING {
      boolean enable_projects
      string project_visibility "curated|full?"
      string resume_url
    }

    MODE_PROJECT_PROMOTION {
      boolean enable_projects
      string project_visibility "curated|full?"
      boolean highlight_pypi
    }

    MODE_SELF_PROMOTION {
      boolean enable_talks
      boolean enable_posts
      boolean highlight_blog
    }

    LANGUAGE_CONFIG {
      string default_language
      string supported_languages "array"
    }

    IDENTITY {
      string name
      string tagline
      string location
      string pypi_username
      string github_username
    }

    IDENTITY_CONTENT {
      string skills_intro
      string projects_intro
      string job_hunting_intro
    }

    RESUME {
      string id
      string label
      string url
      string format       "pdf|docx|html|md|other"
      string audience
      string status       "active|expired|draft"
      string valid_from   "YYYY-MM"
      string description
      string icon
    }

    IDENTITY_RESUME_REF {
      string label
      string url
      string description
      string icon
      string resume_id    "optional FK to RESUME.id"
    }

    TALK {
      string title
      string url
      string icon
    }

    SKILL_CATEGORY {
      string category
      int sort_order "optional"
    }

    SKILL {
      string name
      string level "Expert|Very Good|Good enough|..."
      string icon
    }

    PROFILE {
      string service
      string handle
      string url
      string group  "social|verified|..."
      string icon
    }

    PROJECT {
      string slug  "unique"
      string name
      string description
      string url
      string repository_url
      string status
      string primary_language
    }

    PROJECT_CMS {
      boolean suppress
      string package_links "array"
    }

    PYPI_PACKAGE {
      string package_name "unique"
      int downloads_monthly
      string version
      string summary
      string docs_url
      date last_updated
      string github_repo
    }

    WORK_EXPERIENCE {
      string id "unique"
      string organization
      string title
      string employment_type
      string start_date "YYYY-MM"
      string end_date   "YYYY-MM|present"
      string summary
    }

    EXPERIENCE_RESPONSIBILITY {
      string text
      int sort_order
    }

    EXPERIENCE_TECHNOLOGY {
      string name
      int sort_order
    }

    EXPERIENCE_LINK {
      string label
      string url
      int sort_order
    }

    TAG {
      string name "unique"
    }

    PROJECT_TAG {
      string project_slug "FK"
      string tag_name     "FK"
    }

    PACKAGE_TAG {
      string package_name "FK"
      string tag_name     "FK"
    }
```

## File: src\\github_is_my_cms\\audit_links.py

```python
# src/github_is_my_cms/audit_links.py
import logging
from typing import Set

from github_is_my_cms.builder import SiteBuilder

# Configure basic logging to console
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("auditor")


def run_audit():
    # 1. Initialize Builder to load config and map relationships
    # We use the builder because it already contains the logic for
    # normalizing tags and mapping aliases.
    builder = SiteBuilder()

    # Force the mapping logic to run so populated properties exist
    builder._map_relationships()

    config = builder.config

    print("--- 🔍 Data Link Audit 🔍 ---\n")

    # --- SET UP SETS ---

    # A. All Defined Skills (The Source of Truth)
    # Store tuples of (normalized_name, original_obj)
    defined_skills = {}
    all_aliases = set()

    for group in config.identity.skills:
        for skill in group.skills:
            norm_name = skill.name.lower()
            defined_skills[norm_name] = skill
            all_aliases.add(norm_name)
            if skill.aliases:
                all_aliases.update(a.lower() for a in skill.aliases)

    # B. All Project Tags (From GitHub & PyPI)
    used_tags = set()
    project_counts = {name: 0 for name in defined_skills.keys()}

    all_projects = config.projects + config.pypi_packages

    for item in all_projects:
        # Collect tags
        tags = getattr(item, "tags", []) or []
        for t in tags:
            used_tags.add(t.lower())

        # Collect language
        lang = getattr(item, "primary_language", None)
        if lang:
            used_tags.add(lang.lower())

        # Check which skills map to this project (using Builder's logic)
        # builder.projects_by_skill is { 'Skill Name': [prog1, proj2] }
        for skill_name, projs in builder.projects_by_skill.items():
            if item in projs:
                project_counts[skill_name.lower()] += 1

    # C. All Resume Technologies
    resume_techs = set()
    for exp in config.work_experience:
        for tech in exp.technologies:
            resume_techs.add(tech.lower())

    # --- REPORT 1: Unlinked Tags ---
    # Tags appearing in Projects that map to NO skill
    # (These are likely noise, OR missing skills)

    unlinked_tags = used_tags - all_aliases
    # Filter out obvious noise? (Optional)

    print(f"1. 🏷️  Orphan Tags ({len(unlinked_tags)} found)")
    print("   (Tags in projects that don't match any Skill or Alias)")
    if unlinked_tags:
        # Sort and print first 10
        sorted_orphans = sorted(list(unlinked_tags))
        print(f"   Examples: {', '.join(sorted_orphans[:15])}...")
    else:
        print("   ✅ Clean! All tags map to a skill.")
    print("-" * 40)

    # --- REPORT 2: Skills without Projects ---
    # Skills defined in Identity that have 0 matching projects

    empty_skills = [name for name, count in project_counts.items() if count == 0]

    print(f"2. 👻 Ghost Skills ({len(empty_skills)} found)")
    print("   (Skills defined in Identity but found in ZERO projects)")
    if empty_skills:
        for s in sorted(empty_skills):
            print(f"   - {defined_skills[s].name}")
    else:
        print("   ✅ Robust! Every skill has at least one project.")
    print("-" * 40)

    # --- REPORT 3: Unlinked Resume Tech ---
    # Technologies listed in Resume that don't match a Skill ID

    unlinked_resume_tech = resume_techs - all_aliases

    print(f"3. 📄 Unlinked Resume Technologies ({len(unlinked_resume_tech)} found)")
    print("   (Tech listed in Work Experience that won't hyperlink)")
    if unlinked_resume_tech:
        for t in sorted(list(unlinked_resume_tech)):
            print(f"   - '{t}'")
    else:
        print("   ✅ Connected! All resume tech links to a skill page.")
    print("-" * 40)


if __name__ == "__main__":
    run_audit()
```

## File: src\\github_is_my_cms\\builder.py

```python
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
        self.build_static_api()
        self.build_markdown_pages()
        self.build_html_pages()
        self.build_skill_pages()

        logger.info("Build complete.")


if __name__ == "__main__":
    builder = SiteBuilder()
    builder.build()
```

## File: src\\github_is_my_cms\\cli.py

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
        builder.build_skill_pages()
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

## File: src\\github_is_my_cms\\config.py

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

## File: src\\github_is_my_cms\\data_sources.py

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
            "name,description,url,isArchived,repositoryTopics,homepageUrl,primaryLanguage",
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

                # ADDED: Extract keywords. PyPI sends them as a string "tag1, tag2" or list.
                raw_keywords = info.get("keywords", [])
                tags = []
                if isinstance(raw_keywords, str):
                    # specific cleanup for PyPI keyword strings
                    if raw_keywords:
                        tags = [
                            k.strip() for k in raw_keywords.replace(",", " ").split()
                        ]
                elif isinstance(raw_keywords, list):
                    tags = raw_keywords

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
                    "tags": tags,
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

            # Format is usually {"primaryLanguage": {"name": "Python"}} or null
            prim_lang = repo.get("primaryLanguage", {}) or {}
            language_name = prim_lang.get("name", "N/A")  # e.g. "Python" or None

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
                entry["primary_language"] = language_name

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
                    "primary_language": language_name,
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

            # Ensure 'tags' exists even if fetch failed
            if "tags" not in pkg_data:
                pkg_data["tags"] = []
            updated_list.append(pkg_data)

        # 4. Sort and Save
        updated_list.sort(key=lambda x: x["package_name"].lower())

        with open(self.pypi_file, "wb") as f:
            tomli_w.dump({"packages": updated_list}, f)

        logger.info(
            f"Successfully updated {self.pypi_file} with {len(updated_list)} packages."
        )
```

## File: src\\github_is_my_cms\\generate_skills.py

```python
# src/github_is_my_cms/generate_skills.py
import logging
from collections import defaultdict
from pathlib import Path

import tomli_w

from github_is_my_cms.builder import SiteBuilder

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("generator")


def normalize(text: str) -> str:
    return text.lower().strip()


def run_generation():
    print("--- 🏭 Skills Data Migration & Generation 🏭 ---\n")

    # 1. Load current state
    builder = SiteBuilder()
    # Force the map logic to run so we can access project relationships if needed,
    # though mostly we need the raw config here.
    builder._map_relationships()
    config = builder.config

    # Data Structures for the new file
    # Format: { "Category Name": [ {name="Python", aliases=[], ...} ] }
    new_skill_tree = defaultdict(list)

    # Lookup set to prevent duplicates (stores normalized names AND aliases)
    known_terms = set()

    # --- STEP 1: MIGRATE EXISTING SKILLS ---
    print(f"1. Migrating existing skills from identity.toml...")
    count_existing = 0
    for group in config.identity.skills:
        cat_name = group.category
        for skill in group.skills:
            # Add to lookup
            known_terms.add(normalize(skill.name))
            if skill.aliases:
                for a in skill.aliases:
                    known_terms.add(normalize(a))

            # Prepare dict for TOML output
            skill_data = {
                "name": skill.name,
                "featured": skill.featured,
            }
            if skill.level:
                skill_data["level"] = skill.level
            if skill.icon:
                skill_data["icon"] = skill.icon
            if skill.aliases:
                skill_data["aliases"] = skill.aliases

            new_skill_tree[cat_name].append(skill_data)
            count_existing += 1

    print(f"   Mapped {count_existing} existing skills.\n")

    # --- STEP 2: CAPTURE RESUME TECHNOLOGIES ---
    print(f"2. Scanning Resume Technologies...")
    count_resume_new = 0

    for exp in config.work_experience:
        for tech in exp.technologies:
            norm_tech = normalize(tech)

            if norm_tech not in known_terms:
                # IT'S NEW! Add it.
                print(f"   [+] Found new skill in Resume: {tech}")

                new_skill_entry = {
                    "name": tech,
                    "level": "Competent",  # Default placeholder
                    "featured": True,
                    "aliases": [],  # Initialize empty list for user to fill
                }

                # Add to "Uncategorized" or a specific bucket for manual sorting
                new_skill_tree["Inbox - From Resume"].append(new_skill_entry)

                # Add to known terms so we don't add it twice
                known_terms.add(norm_tech)
                count_resume_new += 1

    if count_resume_new == 0:
        print("   All resume technologies are already covered.")

    # --- STEP 3: CAPTURE PRIMARY LANGUAGES (GitHub) ---
    print(f"\n3. Scanning GitHub Primary Languages...")
    count_lang_new = 0

    for proj in config.projects:
        # Check Primary Language
        lang = getattr(proj, "primary_language", None)
        if lang and lang != "N/A":
            norm_lang = normalize(lang)

            if norm_lang not in known_terms:
                # IT'S NEW! Add it.
                print(f"   [+] Found new skill in GitHub: {lang}")

                new_skill_entry = {
                    "name": lang,
                    "level": "Competent",
                    "featured": True,
                    "icon": "💻",
                    "aliases": [],
                }

                new_skill_tree["Inbox - From GitHub"].append(new_skill_entry)
                known_terms.add(norm_lang)
                count_lang_new += 1

    if count_lang_new == 0:
        print("   All primary languages are already covered.")

    # --- STEP 4: IDENTIFY ORPHAN TAGS (REPORT ONLY) ---
    # We do NOT add these to the file automatically, as they are often garbage.
    print(f"\n4. 🏷️  Orphan Tags Report (For your manual review)")

    all_projects = config.projects + config.pypi_packages
    used_tags = set()

    for item in all_projects:
        tags = getattr(item, "tags", []) or []
        for t in tags:
            used_tags.add(normalize(t))

    orphans = used_tags - known_terms

    if orphans:
        print(
            f"   The following {len(orphans)} tags appear in projects but map to NO skill:"
        )
        print(f"   (If these are skills, add them to 'aliases' in the generated file)")
        print("   ---------------------------------------------------------------")
        # Print in columns
        sorted_orphans = sorted(list(orphans))
        # Simple column print
        for i in range(0, len(sorted_orphans), 3):
            print("   " + "  |  ".join(f"{x:<20}" for x in sorted_orphans[i : i + 3]))
        print("   ---------------------------------------------------------------")
    else:
        print("   ✅ Clean! All project tags map to skills.")

    # --- STEP 5: WRITE FILE ---
    print(f"\n5. Generating data/skills.new.toml...")

    # Convert dictionary to TOML structure list
    # [[skills]] -> category = "X", skills = [...]
    toml_structure = {"skills": []}

    # Sort categories (Keep existing ones first if possible, or alphabetize)
    for category, items in new_skill_tree.items():
        toml_structure["skills"].append({"category": category, "skills": items})

    output_path = Path("data/skills.new.toml")

    with open(output_path, "wb") as f:
        tomli_w.dump(toml_structure, f)

    print(f"   ✅ Success. File written to {output_path}")
    print("   NEXT STEPS:")
    print("   1. Inspect data/skills.new.toml")
    print("   2. Move items from 'Inbox' categories to real categories.")
    print("   3. Add aliases to link the Orphan Tags listed above.")
    print("   4. Rename data/skills.new.toml -> data/skills.toml")
    print("   5. Update builder.py to load 'skills.toml' instead of 'identity.toml'")


if __name__ == "__main__":
    run_generation()
```

## File: src\\github_is_my_cms\\models.py

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

    aliases: List[str] = Field(default_factory=list)

    page_slug: Optional[str] = None

    featured: bool = False

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

    primary_language: Optional[str] = None
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
    tags: List[str] = Field(default_factory=list)


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

## File: src\\github_is_my_cms\\templates\\professional\\components\\identity_graph.md.j2

```
### Connect

{% for profile in identity.profiles %}
* **{{ profile.service|title }}**: [{{ profile.handle }}]({{ profile.url }})
{%- endfor %}

{% if config.modes.current == "job_hunting" and config.modes.job_hunting.resume_url %}
* **Resume**: [Download PDF]({{ config.modes.job_hunting.resume_url }})
{% endif %}
```

## File: src\\github_is_my_cms\\templates\\professional\\layouts\\master.html.j2

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

## File: src\\github_is_my_cms\\templates\\professional\\layouts\\master.md.j2

```
# {{ identity.name }}
{{ identity.tagline }} | {{ identity.location }}
[Home](../../README.md) • [Projects](projects.md) • [API](../apis/openapi.yaml)

---

{% block body %}{% endblock %}

---
*Generated by github-is-my-cms | {{ generation.generated_at }}*
```

## File: src\\github_is_my_cms\\templates\\professional\\pages\\index.html.j2

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
                        {# --- FIX: Check for page_slug and Link --- #}
                        {% if skill.page_slug %}
                            <a href="skills/{{ skill.page_slug }}.html" style="text-decoration: none; border-bottom: 1px dotted #666; color: #000;">
                                {{ skill.name }}
                            </a>
                        {% else %}
                            {{ skill.name }}
                        {% endif %}
                        {# ----------------------------------------- #}

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
                    <div class="tags">
                        <strong>Tech:</strong>
                        {% for tech in role.technologies %}
                            {% set tech_lower = tech|lower %}

                            {# --- FIX: Link Resume Tech to Skill Page --- #}
                            {% if skill_lookup_map and tech_lower in skill_lookup_map %}
                                <a href="skills/{{ skill_lookup_map[tech_lower] }}.html" style="color: #444;">
                                    {{ tech }}
                                </a>
                            {% else %}
                                {{ tech }}
                            {% endif %}
                            {# ------------------------------------------- #}

                            {% if not loop.last %}, {% endif %}
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

## File: src\\github_is_my_cms\\templates\\professional\\pages\\projects.html.j2

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

## File: src\\github_is_my_cms\\templates\\professional\\pages\\projects.md.j2

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

## File: src\\github_is_my_cms\\templates\\professional\\pages\\README.en.md.j2

```
{% extends "layouts/master.md.j2" %}
{# --- MACRO DEFINITIONS --- #}
{% macro section_talks() %}
## Talks & Presentations
{% for talk in identity.talks %}
{{ talk.icon or "▶️" }} [{{ talk.title }}]({{ talk.url }})<br>
{% endfor %}
{% endmacro %}


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
{# Important! No Leading whitepspace, this messes up the markdown formatter, etc. #}
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

## File: src\\github_is_my_cms\\templates\\professional\\pages\\skill_detail.html.j2

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
    {% for item in skill_projects %}
    <article>
        <header>
            {# Handle Polymorphism: GitHub Project vs PyPI Package #}
            {% set name = item.name if item.name is defined else item.package_name %}
            {% set url = item.url or item.repository_url or item.docs_url or ('https://pypi.org/project/' ~ name) %}

            <strong><a href="{{ url }}">{{ name }}</a></strong>

            {# Optional Badge to distinguish type #}
            {% if item.package_name is defined %}
                <span class="meta" style="font-size:0.7rem; border:1px solid #ddd; padding:2px 4px; border-radius:3px;">PyPI</span>
            {% endif %}
        </header>

        <p>
            {{ item.description if item.description is defined else item.summary }}
        </p>

        <footer>
            <small>
                {% for tag in item.tags %}
                    {% if tag|lower == skill_name|lower %}
                        <strong>#{{ tag }}</strong>
                    {% else %}
                        #{{ tag }}
                    {% endif %}
                {% endfor %}

                {# Explicitly show language if available on GitHub projects #}
                {% if item.primary_language and item.primary_language|lower == skill_name|lower %}
                     <strong>#{{ item.primary_language }}</strong>
                {% elif item.primary_language %}
                     #{{ item.primary_language }}
                {% endif %}
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
