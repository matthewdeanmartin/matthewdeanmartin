"""
config.py
Configuration loader for the README CMS.
Responsible for reading TOML files and instantiating the CMSConfig model.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Dict, Any

# Use tomllib for Python 3.11+, fallback to tomli for older versions if needed.
# Since the GHIP is dated 2025, we assume Python 3.11+ is standard.
if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("Python 3.11+ or 'tomli' package is required.")

from .models import CMSConfig


class ConfigLoader:
    """
    Loads and merges data from multiple TOML sources as defined in GHIP-001.
    """

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.data_dir = self.root_dir / "src" / "readme_maker" / "data"
        self.config_file = self.root_dir / "readme_cms.toml"

    def _load_toml_file(self, filepath: Path) -> Dict[str, Any]:
        """Helper to safely load a TOML file if it exists."""
        if not filepath.exists():
            return {}
        with open(filepath, "rb") as f:
            return tomllib.load(f)

    def load(self) -> CMSConfig:
        """
        Aggregates all data sources into a single validated CMSConfig object.
        """
        # 1. Load Main Config (readme_cms.toml)
        # Contains: modes, languages
        main_config = self._load_toml_file(self.config_file)

        # 2. Load Identity Data (identity.toml & identity_graph.toml)
        # GHIP separates these, but our Identity model aggregates them.
        identity_data = self._load_toml_file(self.data_dir / "identity.toml")
        graph_data = self._load_toml_file(self.data_dir / "identity_graph.toml")

        # Merge identity graph into the main identity dict under 'profiles'
        # Expectation: identity.toml has basic info (name, tagline),
        # identity_graph.toml has specific social nodes.
        if "identities" in graph_data:
            # The model expects 'profiles', the file might name it 'identities'
            # per the example in the GHIP "Identity Graph" section.
            identity_data["profiles"] = graph_data["identities"]

        # 3. Load Projects (projects.toml)
        # Manually curated projects
        projects_data = self._load_toml_file(self.data_dir / "projects.toml")
        projects_list = projects_data.get("projects", [])

        # 4. Load PyPI Metadata (pypi_projects.toml)
        # Automated data from weekly workflow
        pypi_data = self._load_toml_file(self.data_dir / "pypi_projects.toml")
        pypi_list = pypi_data.get("packages", [])

        # 5. Assemble the final dictionary for Pydantic validation
        # We merge all top-level keys.
        config_dict = {
            "identity": identity_data,
            "modes": main_config.get("mode", {}),  # GHIP uses [mode] table
            "languages": main_config.get("languages", {}),
            "projects": projects_list,
            "pypi_packages": pypi_list
        }

        # 6. Validate and Return
        # This triggers all Pydantic validators, including "No Twitter/X".
        return CMSConfig(**config_dict)


def load_config(root_path: str = ".") -> CMSConfig:
    """Convenience entry point."""
    return ConfigLoader(Path(root_path)).load()