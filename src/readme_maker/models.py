"""
models.py
Data structures for the Multi-Page, Mode-Aware GitHub README CMS.
Implements schema validation and JSON serialization for the Static API.
"""
from __future__ import  annotations
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator

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

# --- Identity Models ---

class SocialProfile(BaseModel):
    """
    Represents a node in the Identity Graph.
    """
    service: str = Field(..., description="Name of the service (e.g., github, linkedin)")
    handle: str = Field(..., description="Username or handle")
    url: HttpUrl = Field(..., description="Link to the profile")
    same_as: List[HttpUrl] = Field(default_factory=list, description="List of equivalent URLs for JSON-LD")

    @field_validator('url', 'service')
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
    profiles: List[SocialProfile] = Field(default_factory=list, description="The Identity Graph")

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
    project_promotion: ProjectPromotionSettings = Field(default_factory=ProjectPromotionSettings)
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