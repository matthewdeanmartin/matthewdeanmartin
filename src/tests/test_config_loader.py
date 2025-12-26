from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from github_is_my_cms.config import ConfigLoader, assign_groups


def _write_text(path: Path, content: str) -> None:
    path.write_text(dedent(content), encoding="utf-8")


def _write_minimal_config(root: Path) -> None:
    data_dir: Path = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    _write_text(
        root / "readme_cms.toml",
        """
        [mode]
        current = "project_promotion"

        [languages]
        default = "en"
        supported = ["en"]
        """,
    )

    _write_text(
        data_dir / "identity.toml",
        """
        name = "Example Person"
        tagline = "Example Tagline"

        [[skills]]
        category = "Legacy"
        [[skills.skills]]
        name = "Legacy Skill"
        """,
    )

    _write_text(
        data_dir / "projects.toml",
        """
        [[projects]]
        slug = "project-one"
        name = "Project One"
        description = "Example project"
        tags = ["cli"]
        primary_language = "Python"
        """,
    )

    _write_text(
        data_dir / "pypi_projects.toml",
        """
        packages = []
        """,
    )

    _write_text(
        data_dir / "work_experience.toml",
        """
        experience = []
        """,
    )


def test_assign_groups_sets_tag_and_language_defaults() -> None:
    projects: list[dict[str, object]] = [
        {
            "name": "Alpha",
            "tags": ["cli", "tools"],
            "primary_language": "Python",
        },
        {
            "name": "Beta",
            "tags": [],
            "primary_language": "Go",
        },
        {
            "name": "Gamma",
            "tags": [],
        },
    ]

    assign_groups(projects)

    assert projects[0]["group"] == "Cli"
    assert projects[1]["group"] == "Go"
    assert projects[2]["group"] == "Other"


def test_config_loader_uses_skills_toml_when_present(tmp_path: Path) -> None:
    _write_minimal_config(tmp_path)

    _write_text(
        tmp_path / "data" / "skills.toml",
        """
        [[skills]]
        category = "New Skills"
        [[skills.skills]]
        name = "New Skill"
        """,
    )

    config = ConfigLoader(tmp_path).load()

    assert config.identity.skills[0].category == "New Skills"
    assert config.identity.skills[0].skills[0].name == "New Skill"


def test_config_loader_converts_legacy_resumes(tmp_path: Path) -> None:
    _write_minimal_config(tmp_path)

    _write_text(
        tmp_path / "data" / "identity.toml",
        """
        name = "Example Person"
        tagline = "Example Tagline"

        [[resumes]]
        label = "Legacy Resume"
        url = "https://example.com/resume.pdf"
        description = "Legacy"
        icon = "📄"
        """,
    )

    config = ConfigLoader(tmp_path).load()

    assert len(config.resumes) == 1
    assert config.resumes[0].id == "legacy-0"
    assert config.resumes[0].label == "Legacy Resume"
    assert config.resumes[0].format.value == "other"
