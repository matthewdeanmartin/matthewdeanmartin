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
