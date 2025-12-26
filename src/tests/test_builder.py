from __future__ import annotations

from pathlib import Path
from textwrap import dedent

from github_is_my_cms.builder import SiteBuilder


def _write_text(path: Path, content: str) -> None:
    path.write_text(dedent(content), encoding="utf-8")


def _write_builder_fixture(root: Path) -> None:
    data_dir: Path = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    templates_dir: Path = root / "src" / "github_is_my_cms" / "templates" / "default"
    templates_dir.mkdir(parents=True, exist_ok=True)

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
        """,
    )

    _write_text(
        data_dir / "skills.toml",
        """
        [[skills]]
        category = "Languages"
        [[skills.skills]]
        name = "Python"
        aliases = ["py"]
        """,
    )

    _write_text(
        data_dir / "projects.toml",
        """
        [[projects]]
        slug = "project-one"
        name = "Project One"
        description = "Example project"
        tags = ["py"]
        primary_language = "Go"
        """,
    )

    _write_text(
        data_dir / "pypi_projects.toml",
        """
        [[packages]]
        package_name = "example-pkg"
        summary = "Example package"
        """,
    )

    _write_text(
        data_dir / "work_experience.toml",
        """
        experience = []
        """,
    )

    _write_text(
        data_dir / "resumes.toml",
        """
        resumes = []
        """,
    )


def test_builder_maps_skill_relationships(tmp_path: Path) -> None:
    _write_builder_fixture(tmp_path)

    builder = SiteBuilder(str(tmp_path))
    builder._map_relationships()

    python_projects = builder.projects_by_skill.get("Python")

    assert python_projects is not None
    assert {item.__class__.__name__ for item in python_projects} == {
        "Project",
        "PyPIPackage",
    }
    assert builder.skill_lookup_map["py"] == "python"
