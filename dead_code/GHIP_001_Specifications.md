## GHIP: 001 Title: "github-is-my-cms", a multipage job search and project promotion site generator Author: Matthew Dean Martin Status: Draft Type: Standards Track Created: 2025-12-07 Requires: None

## Abstract

This GHIP defines a Python-based content management system (CMS) for GitHub profile repositories that:

- Generates a **mode-aware**, **multi-page** documentation set.
- Keeps the repository root minimal while storing content and build artefacts under `src/` and `docs/`.
- Uses **TOML** for structured data and Markdown (`.md`) for prose content.
- Renders Markdown via **Jinja** templates with a **master page** (header/footer) and reusable **components**.
- Supports **identity graph** correlation, resume links, side project groups, and multiple “persona modes”.
- Provides **multi-language support** with LLM-based translations and language switchers.
- Exposes a **static API** described by an OpenAPI/Swagger document, backed by static files so that a hypothetical javascript app could call all the endpoints get data formats and then create a dynamic javascript front end as a SPA.
- Generates both Markdown and HTML, suitable for GitHub’s Markdown view and GitHub Pages.
- Is refreshed weekly by GitHub Actions: updating TOML metadata from PyPI/GitHub, recompiling content, regenerating translations, and publishing GitHub Pages.

The goal is a system where the GitHub profile is equally usable as Markdown or HTML and can be kept fresh via automated jobs.

## Motivation

GitHub profile READMEs are typically one-off, hand-edited single pages. This leads to:

- Overloaded READMEs trying to be **CV**, **project catalog**, and **personal site** simultaneously.
- No clear separation between **data** (identities, projects, links) and **content** (descriptions, long form text).
- Weak **internationalization**, limited to manually maintained translated READMEs.
- Redundant and error-prone manual updates to links, projects, and metadata.
- No systematic way to present different **modes** (job hunting vs project promotion vs self promotion) without rewriting content.
- No structured way to surface content via **machine-readable APIs** (e.g. static JSON + OpenAPI).

A minimal but opinionated CMS that compiles multiple Markdown and HTML pages from structured TOML and Markdown content solves these problems while staying within GitHub’s normal workflows.

## Goals and Non-Goals

### Goals

1. **Multi-page design**: Support multiple Markdown documents with navigational links from the root `README.md`.

1. **Minimal root layout**: Keep the repository root uncluttered: only `.github/`, `src/`, `docs/`, and `README.md`.

1. **Mode awareness**:

   - Job Hunting Mode
   - Project Promotion Mode
   - Self Promotion Mode

1. **Language switching**:

   - Language index like:

     ```markdown
     ## Languages
     - [English](README.en.md)
     - [Español](README.es.md)
     - [Français](README.fr.md)
     ```

   - LLM-based translation using an OpenAI-compatible tool.

1. **Master page + components**:

   - Shared header/footer.
   - Reusable components such as `identity_graph.md`.

1. **Data vs content separation**:

   - **Data** in TOML: identity graph, PyPI projects, PyPI→GitHub mappings, cached metadata.
   - **Content** in Markdown: project descriptions, long-form sections, etc.

1. **Static API + Swagger**:

   - OpenAPI spec describing static endpoints for JSON/Markdown assets.
   - Generated HTML Swagger UI under `docs/`.

1. **Weekly automation**:

   - Regenerate TOML from PyPI/GitHub.
   - Recompile all pages (Markdown and HTML).
   - Regenerate translations via LLM.
   - Publish GitHub Pages.

1. **No Twitter/X**:

   - Do not surface Twitter/X links in generated content.

### Non-Goals

- Not a generic documentation generator for arbitrary repos.
- Not a headless CMS for arbitrary backends; scope is a single GitHub profile repo.
- Not a live server; all artefacts are static files.

## Repository Layout

The recommended directory structure:

```text
.github/
    workflows/
        readme_cms.yml       # Scheduled GitHub Actions workflow

src/
    github_is_my_cms/           # Python package (core CMS)
        __init__.py
        cli.py
        config.py
        models.py
        data_sources/
        templates/
            layouts/        # Master page templates
            components/     # Reusable blocks (e.g. identity_graph)
            pages/          # Jinja templates for each Markdown target
    content/                # Source Markdown content (author-edited)
        projects/
            *.md
        posts/
            *.md
        pages/
            about.md
            now.md
            talks.md
        identity_graph.md   # Optional manually-authored component content

docs/
    img/                    # Images used in README and docs
    md/                     # Compiled Markdown pages (multi-page README content)
        README.en.md
        README.es.md
        README.fr.md
        about.md
        projects.md
    apis/                   # Static API payloads and OpenAPI spec
        openapi.yaml
        identity.json
        projects.json
        activity.json
    index.html              # GitHub Pages entrypoint (HTML)
    ...                     # Additional HTML pages

README.md                   # Root profile README (links into docs/md/*)
pyproject.toml              # Python project config
readme_cms.toml             # CMS configuration
```

Constraints:

- Root directory should not contain arbitrary extra files beyond:

  - `.github/`
  - `src/`
  - `docs/`
  - `README.md`
  - Standard Python packaging files (`pyproject.toml`, etc.).

- All long-form content lives under `src/content/` and is compiled into `docs/md/` and HTML.

## Modes

The CMS supports three operational modes, which control which sections are rendered, their prominence, and sometimes their tone:

1. **Job Hunting Mode**

   - Emphasis:

     - Resume links and CV-like information.
     - Skills, experience, notable achievements.
     - Contact channels suitable for recruiters.

   - Features:

     - Prominent “Hire Me” or “Open to roles” section.
     - Reduced experimental/archived projects, focus on production-quality work.

1. **Project Promotion Mode**

   - Emphasis:

     - Active side projects, OSS contributions, libraries.

   - Features:

     - Larger “Projects” section with grouped subsections.
     - Clear links to GitHub repositories and PyPI packages.
     - Static API exposing project metadata.

1. **Self Promotion Mode**

   - Emphasis:

     - Personal brand: writing, talks, podcasts, community involvement.

   - Features:

     - Links to blog posts, talks, and external appearances.
     - “Identity graph” highlighting cross-platform presence.
     - Note: still must obey “no Twitter/X” output requirement.

### Mode Configuration

`readme_cms.toml` may include:

```toml
[mode]
current = "job_hunting"  # one of: "job_hunting", "project_promotion", "self_promotion"

[mode.job_hunting]
enable_projects = true
project_visibility = "curated"  # curated | minimal | full

[mode.project_promotion]
enable_projects = true
project_visibility = "full"
highlight_pypi = true

[mode.self_promotion]
enable_talks = true
enable_posts = true
```

Mode selection affects:

- Which pages are generated.
- Which sections appear in `README.*.md`.
- Ordering and emphasis within pages.

## Data and Content Sources

### Data (TOML)

All structured metadata is stored as TOML under `src/github_is_my_cms/data/` (or similar):

- `identity.toml`

  - Name, tagline, location.
  - Allowed social links (no Twitter/X).
  - Contact methods.
  - Identity graph linking multiple sites.

- `identity_graph.toml`

  - Machine-readable identity graph:

    - GitHub, GitLab, LinkedIn, resume URL(s), StackOverflow, blog, etc.
    - `same_as` lists suitable for JSON-LD export.

- `projects.toml`

  - Manually curated projects with grouping and status.

- `pypi_projects.toml`

  - List of PyPI packages and mapping to GitHub repositories.
  - Cached metadata from PyPI (version, summary, downloads if available).

- `config.toml` / `readme_cms.toml`

  - CMS configuration, mode selection, languages, templates.

These files are **regenerated or updated** by the weekly workflow where appropriate (specifically for PyPI/GitHub-derived metadata).

### Content (Markdown)

Markdown content is stored under `src/content/`:

- `pages/*.md`

  - Essays or static pages (“About”, “Now”, etc.).

- `projects/*.md`

  - Detailed project descriptions, one file per project or group.

- `posts/*.md`

  - Optional short posts or highlights.

- `identity_graph.md`

  - A human-readable representation of the identity graph (component).

These files are **author-edited** and never overwritten by automation.

## Templating and Master Page Design

### Jinja Templates

Jinja is used for all templating. Templates are organized as:

- `layouts/master.md.j2`

  - Provides a master Markdown layout with header/footer and named blocks.

- `layouts/master.html.j2`

  - Parallel master for HTML output.

- `components/*.md.j2`

  - Reusable components such as identity graph, project lists, badges.

- `pages/*.md.j2`

  - Page-specific layouts (e.g. `README.md.j2`, `projects.md.j2`).

Example master Markdown template:

```jinja
{# layouts/master.md.j2 #}
{{ header }}

{% block body %}{% endblock %}

{{ footer }}
```

Example page template:

```jinja
{# pages/README.en.md.j2 #}
{% extends "layouts/master.md.j2" %}

{% block body %}
# {{ identity.name }}

{{ identity.tagline }}

{% include "components/language_switcher.md.j2" %}

{% include "components/identity_graph.md.j2" %}

{% if mode.job_hunting %}
{% include "components/job_hunting_summary.md.j2" %}
{% endif %}

{% if mode.project_promotion %}
{% include "components/project_overview.md.j2" %}
{% endif %}

{% if mode.self_promotion %}
{% include "components/self_promo_summary.md.j2" %}
{% endif %}
{% endblock %}
```

The same data is rendered twice: once into Markdown templates and once into HTML templates for GitHub Pages.

### Components

Components are modular Jinja snippets. Examples:

- `identity_graph.md.j2`
- `project_card.md.j2`
- `resume_links.md.j2`
- `talks_list.md.j2`

Components can be reused across pages and modes.

## Language Support and Translation

### Language Index

Each generated README includes a language selector:

```markdown
## Languages

- [English](README.en.md)
- [Español](README.es.md)
- [Français](README.fr.md)
```

Additional languages can be enabled in `readme_cms.toml`:

```toml
[languages]
default = "en"
supported = ["en", "es", "fr"]
```

### Translation Workflow

- Source language is the default (`en`).

- Author edits only the canonical Markdown templates and content in the source language.

- The weekly workflow:

  1. Compiles the source-language Markdown pages.
  1. Runs translations using a configured LLM provider (OpenAI-compatible).
  1. Writes translated Markdown pages to `docs/md/README.<lang>.md`, etc.

- Translation metadata (e.g. last translated timestamp, source hash) may be persisted in TOML or JSON to avoid unnecessary re-translation.

### Translation Tool

The translation component:

- Accepts:

  - Source Markdown.
  - Target language code.
  - Optional style guidelines.

- Returns:

  - Translated Markdown with the same structural headings and links.

- Enforces:

  - Preserving code blocks.
  - Preserving URLs.
  - Preserving specific tokens (e.g. project names, package names).

Implementation detail: the tool is a Python wrapper around the LLM client, abstracted so providers can be swapped.

## Identity Graph

The system defines an identity graph that correlates user identities across services:

- Stored in `identity_graph.toml`.

- Rendered as:

  - Human-readable Markdown component.
  - Machine-readable JSON (e.g. `docs/apis/identity.json`).
  - Optional JSON-LD snippet (embedded as fenced code block in README).

Constraints:

- No Twitter/X entries. The CMS should:

  - Ignore any identities with `domain` in `{ "twitter.com", "x.com" }`.
  - Optionally warn if such entries are present in TOML.

Example TOML:

```toml
[[identities]]
service = "github"
handle = "example"
url = "https://github.com/example"

[[identities]]
service = "linkedin"
handle = "example"
url = "https://www.linkedin.com/in/example/"

[[identities]]
service = "website"
handle = "personal-site"
url = "https://example.com"
```

## Static API and Swagger

The system exposes a static API via JSON files under `docs/apis/`, and an OpenAPI/Swagger spec:

- `docs/apis/openapi.yaml`

  - Describes endpoints such as:

    - `/apis/identity.json`
    - `/apis/projects.json`
    - `/apis/activity.json`

- These endpoints are static files served by GitHub Pages.

Example static API payloads:

- `identity.json`: identity graph and basic profile info.
- `projects.json`: project metadata, PyPI/GitHub mappings, status.
- `activity.json`: recent OSS activity snapshot (optional).

### Swagger UI

The HTML swagger page:

- Generated (or referenced) at e.g. `docs/swagger.html`.
- Uses the `openapi.yaml` as its specification.
- Linked from README and/or docs homepage.

## Build and Compilation

### Markdown Compilation

For each configured language and mode, the pipeline:

1. Loads TOML data (identity, projects, PyPI metadata, config).

1. Loads Markdown content from `src/content/`.

1. Renders:

   - Source-language templates via Jinja.
   - Writes resultant Markdown to `docs/md/*.md`.

1. Generates `README.md` in root, which:

   - Points to `docs/md/` for detailed pages.
   - Contains high-level summary plus language index.

### HTML Compilation

Separately, HTML templates render:

1. `docs/index.html` as GitHub Pages entrypoint.
1. HTML equivalents of the Markdown pages (e.g. `docs/README.en.html` or `docs/en/index.html`).
1. Optional HTML version of components where appropriate.

Markdown is treated as the **primary authored format**; HTML is a compiled output, not manually edited.

### Equal Enjoyment in Markdown and HTML

Design constraints:

- Layout and content must be readable in raw `.md` form on GitHub.

- HTML rendering must preserve:

  - Section structure.
  - Navigation via links.
  - Language switching.

No HTML-only features that significantly degrade the Markdown experience should be introduced (e.g. heavy JS-dependent layouts that are meaningless in Markdown).

## Weekly GitHub Actions Workflow

A scheduled GitHub Actions workflow (`.github/workflows/readme_cms.yml`) runs weekly with the following responsibilities:

1. **Regenerate TOML data from PyPI/GitHub**

   - Fetch metadata for PyPI packages:

     - Latest version, summary, link to docs, etc.

   - Resolve PyPI packages to GitHub repositories.

   - Fetch limited metadata from GitHub repositories (stars, last push, etc.).

   - Update `pypi_projects.toml` and related TOML caches.

1. **Recompile content**

   - Run `readme-make build` (CLI name to be defined).
   - Rebuild Markdown pages into `docs/md/`.
   - Rebuild HTML pages into `docs/`.

1. **Regenerate translations**

   - For each non-default language, compare source content hash.
   - Re-translate pages whose source changed.
   - Write updated translated Markdown.

1. **Publish GitHub Pages**

   - Commit changes to `docs/` (if any).
   - Push to main or a designated branch used for Pages.
   - Rely on GitHub Pages to serve `docs/` as the static site.

The workflow must be idempotent and should no-op when no changes are detected.

## Quality Checks

The build system should include a `lint` step that covers:

- **Content and structure**

  - Required sections present for each mode.
  - Heading levels consistent.
  - No empty sections.

- **Links**

  - Validate external links (HTTP 2xx/3xx).
  - Ensure no Twitter/X links in rendered output.
  - Ensure internal links to `docs/md/` and `docs/apis/` are valid.

- **Data consistency**

  - TOML schema validation (e.g. via pydantic models).
  - Identity graph entries must have valid URLs.
  - PyPI→GitHub mappings must be coherent.

- **Output integrity**

  - Generated Markdown parses cleanly.
  - Generated HTML contains expected sections (spot checks or snapshot tests).

Errors should cause the CI job to fail. Warnings can be reported without failing, controlled via config.

## Reference Implementation Sketch

A reference implementation is expected to be a Python package `github_is_my_cms` with:

- CLI using argparse.

- Configuration loading from `readme_cms.toml`.

- Models for:

  - Identity, identities, projects, PyPI packages.

- Template renderer using Jinja.

- Translation adapter for OpenAI-compatible LLM APIs.

- Data source modules for:

  - GitHub API.
  - PyPI JSON API.

- Build commands:

  - `build` – compile Markdown and HTML.
  - `lint` – run quality checks.
  - `translate` – regenerate translations.
  - `update-data` – refresh TOML from remote sources.

## Backwards Compatibility

This GHIP assumes a **new** repository structure for the profile. It does not need to maintain compatibility with an existing ad-hoc README.

Adopters can migrate by:

1. Moving existing README content into `src/content/pages/`.
1. Creating initial TOML identity and project data.
1. Generating new `README.md` and `docs/*` via the CMS.

## Security and Privacy Considerations

- API tokens must be stored only in GitHub Actions secrets or environment variables, not in TOML or committed files.
- Identity graph may expose cross-platform account correlations; users must opt into which identities are public.
- Translation provider choice must comply with user privacy expectations; some users may require self-hosted or EU-hosted providers.

## Rejected Ideas

- Embedding arbitrary JavaScript in Markdown for dynamic behavior (rejected: breaks Markdown-first design and GitHub profile expectations).
- Using non-Markdown authoring formats (e.g. reStructuredText or AsciiDoc) (rejected: poor GitHub profile integration).
- Supporting Twitter/X as first-class identity (rejected per explicit requirement).

______________________________________________________________________

End of GHIP #001.
