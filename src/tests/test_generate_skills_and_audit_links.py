from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest
import tomllib
from _pytest.capture import CaptureFixture

from github_is_my_cms.audit_links import run_audit
from github_is_my_cms.generate_skills import run_generation


def _write_text(path: Path, content: str) -> None:
    path.write_text(dedent(content), encoding="utf-8")


def _write_shared_fixture(root: Path) -> None:
    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    templates_dir = root / "src" / "github_is_my_cms" / "templates" / "default"
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
        featured = true
        """,
    )

    _write_text(
        data_dir / "projects.toml",
        """
        [[projects]]
        slug = "project-one"
        name = "Project One"
        description = "Example project"
        tags = ["py", "lonely-tag"]
        primary_language = "Go"
        """,
    )

    _write_text(
        data_dir / "pypi_projects.toml",
        """
        [[packages]]
        package_name = "example-pkg"
        summary = "Example package"
        tags = ["docs"]
        """,
    )

    _write_text(
        data_dir / "work_experience.toml",
        """
        [[experience]]
        id = "exp-1"
        organization = "Example Org"
        title = "Example Role"
        employment_type = "full_time"
        start_date = "2020-01"
        end_date = "2021-01"
        technologies = ["GraphQL"]
        """,
    )

    _write_text(
        data_dir / "resumes.toml",
        """
        resumes = []
        """,
    )


def test_run_generation_writes_new_skill_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_shared_fixture(tmp_path)
    monkeypatch.chdir(tmp_path)

    run_generation()

    output_path = tmp_path / "data" / "skills.new.toml"
    assert output_path.exists()

    contents = tomllib.loads(output_path.read_text(encoding="utf-8"))
    categories = {item["category"] for item in contents["skills"]}

    assert "Inbox - From Resume" in categories
    assert "Inbox - From GitHub" in categories


def test_run_audit_reports_orphans(
    tmp_path: Path,
    capsys: CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_shared_fixture(tmp_path)
    monkeypatch.chdir(tmp_path)

    run_audit()

    captured = capsys.readouterr().out
    assert "Orphan Tags" in captured
    assert "Ghost Skills" in captured
    assert "Unlinked Resume Technologies" in captured
