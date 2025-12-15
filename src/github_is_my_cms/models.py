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


class Identity(BaseModel):
    """
    Core personal information and aggregation of the identity graph.
    """

    name: str
    tagline: str
    location: Optional[str] = None
    email: Optional[str] = None
    profiles: List[SocialProfile] = Field(
        default_factory=list, description="The Identity Graph"
    )

    # ADDED: New structured data
    resumes: List[ResumeEntry] = Field(default_factory=list)
    skills: List[SkillGroup] = Field(default_factory=list)
    talks: List[TalkEntry] = Field(default_factory=list)

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


class ResumeArtifact(BaseModel):
    id: str
    label: str
    url: HttpUrl
    format: ResumeFormat = ResumeFormat.PDF
    audience: Optional[str] = None
    status: ResumeStatus = ResumeStatus.ACTIVE
    valid_from: Optional[str] = None   # "YYYY-MM" or "YYYY"
    valid_until: Optional[str] = None  # optional
    description: Optional[str] = None
    icon: Optional[str] = "📄"
