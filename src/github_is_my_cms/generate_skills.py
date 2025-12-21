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
