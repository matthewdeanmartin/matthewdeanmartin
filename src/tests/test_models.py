from __future__ import annotations

from github_is_my_cms.models import Identity, Skill, SkillGroup


def test_identity_skill_rows_render_displays() -> None:
    identity = Identity(
        name="Example",
        tagline="Example",
        skills=[
            SkillGroup(
                category="Backend",
                skills=[
                    Skill(name="Python", level="Expert", icon="🐍"),
                    Skill(name="Postgres", icon="🐘"),
                ],
            ),
            SkillGroup(
                category="Frontend",
                skills=[Skill(name="HTMX")],
            ),
        ],
    )

    rows = identity.skill_rows

    assert rows == [
        ["🐍 Python - Expert", "HTMX"],
        ["🐘 Postgres", ""],
    ]


def test_identity_featured_skill_rows_filtering() -> None:
    identity = Identity(
        name="Example",
        tagline="Example",
        skills=[
            SkillGroup(
                category="Devops",
                skills=[
                    Skill(name="Terraform", featured=True),
                    Skill(name="Ansible"),
                ],
            ),
            SkillGroup(
                category="Languages",
                skills=[Skill(name="Python", featured=True)],
            ),
        ],
    )

    rows = identity.featured_skill_rows

    assert rows == [["Terraform", "Python"]]
