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
