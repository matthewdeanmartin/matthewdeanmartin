"""
cli.py
Command-line interface for the Multi-Page, Mode-Aware GitHub README CMS.
Handles argument parsing, logging setup, and command dispatch.
"""

import argparse
import logging
import sys
from typing import List, Optional

# Import the builder (functionality we've already implemented)
from .builder import SiteBuilder

# Versioning (ideally fetched from package metadata in production)
VERSION = "0.1.0"


def setup_logging(level_name: str):
    """
    Configures the root logger based on the user's verbosity selection.
    """
    numeric_level = getattr(logging, level_name.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {level_name}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )


def cmd_build(args: argparse.Namespace):
    """
    Handler for the 'build' subcommand.
    Compiles Markdown and HTML pages.
    """
    logging.info("Starting build process...")
    try:
        builder = SiteBuilder(root_dir=args.root)
        builder.build()
        logging.info("Build completed successfully.")
    except Exception as e:
        logging.error(f"Build failed: {e}", exc_info=True)
        sys.exit(1)


def cmd_lint(args: argparse.Namespace):
    """
    Placeholder: Validates content structure, links, and TOML data.
    """
    logging.warning("Command 'lint' is not yet implemented.")
    logging.info(f"Would scan root: {args.root}")
    # TODO: Implement quality checks defined in GHIP-001 "Quality Checks"


def cmd_translate(args: argparse.Namespace):
    """
    Placeholder: Runs LLM-based translation for non-default languages.
    """
    logging.warning("Command 'translate' is not yet implemented.")
    # TODO: Implement LLM integration defined in GHIP-001 "Translation Workflow"


def cmd_update_data(args: argparse.Namespace):
    """
    Placeholder: Fetches fresh data from PyPI and GitHub APIs.
    """
    logging.warning("Command 'update-data' is not yet implemented.")
    # TODO: Implement fetchers defined in GHIP-001 "Weekly GitHub Actions Workflow"


def main(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="Multi-Page, Mode-Aware GitHub README CMS",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # --- Global Arguments ---
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging verbosity."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Path to the repository root containing readme_cms.toml."
    )

    # --- Subcommands ---
    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        help="Available operations"
    )

    # Command: build
    parser_build = subparsers.add_parser(
        "build",
        help="Compile TOML and Markdown into final docs/ artefacts."
    )
    parser_build.set_defaults(func=cmd_build)

    # Command: lint (Placeholder)
    parser_lint = subparsers.add_parser(
        "lint",
        help="Validate links, content structure, and data integrity."
    )
    parser_lint.set_defaults(func=cmd_lint)

    # Command: translate (Placeholder)
    parser_translate = subparsers.add_parser(
        "translate",
        help="Regenerate translations using configured LLM provider."
    )
    parser_translate.set_defaults(func=cmd_translate)

    # Command: update-data (Placeholder)
    parser_update = subparsers.add_parser(
        "update-data",
        help="Refresh cached data from PyPI and GitHub APIs."
    )
    parser_update.set_defaults(func=cmd_update_data)

    # --- Execution Logic ---

    # Check for empty args (excluding script name) to default to help
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args(argv)

    # Apply logging configuration
    setup_logging(args.log_level)

    # Dispatch to function
    if hasattr(args, "func"):
        args.func(args)
    else:
        # Fallback if valid command structure but no func mapped (unlikely with subparsers)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()