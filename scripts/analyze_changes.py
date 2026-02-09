#!/usr/bin/env python3
"""
Analyze changed webui files and determine which RST docs need updating.

Usage:
  # From a list of changed files (one per line on stdin):
  echo "react/src/pages/DashboardPage.tsx" | python scripts/analyze_changes.py

  # From git diff output:
  git diff --name-only HEAD~1 | python scripts/analyze_changes.py

  # With explicit file arguments:
  python scripts/analyze_changes.py --files react/src/pages/ChatPage.tsx

  # JSON output for CI:
  python scripts/analyze_changes.py --format json --files react/src/pages/ServingPage.tsx
"""

import argparse
import fnmatch
import json
import sys
from pathlib import Path

import yaml


def load_mapping(mapping_path: str) -> dict:
    with open(mapping_path, "r") as f:
        data = yaml.safe_load(f)
    if "pages" not in data:
        raise ValueError("Missing 'pages' section in mapping file")
    return data


def match_glob(pattern: str, filepath: str) -> bool:
    """Match a file path against a glob pattern (supports **)."""
    if "**" in pattern:
        # Convert ** glob to work with fnmatch
        # e.g. "react/src/components/Chat/**" matches "react/src/components/Chat/Foo.tsx"
        base = pattern.replace("/**", "")
        return filepath.startswith(base + "/")
    return fnmatch.fnmatch(filepath, pattern) or filepath == pattern


def find_affected_docs(changed_files: list, mapping: dict) -> dict:
    affected_rst = set()
    matched_sources = {}
    unmatched_files = []

    for changed_file in changed_files:
        file_matched = False

        for page_entry in mapping.get("pages", []):
            for source_pattern in page_entry.get("sources", []):
                if match_glob(source_pattern, changed_file):
                    file_matched = True
                    for doc in page_entry.get("docs", []):
                        affected_rst.add(doc)
                    matched_sources.setdefault(changed_file, []).append(
                        {"type": "page", "route": page_entry["route"]}
                    )

        for comp_entry in mapping.get("components", []):
            for source_pattern in comp_entry.get("sources", []):
                if match_glob(source_pattern, changed_file):
                    file_matched = True
                    for doc in comp_entry.get("docs", []):
                        affected_rst.add(doc)
                    matched_sources.setdefault(changed_file, []).append(
                        {"type": "component", "name": comp_entry["name"]}
                    )

        if not file_matched:
            unmatched_files.append(changed_file)

    return {
        "affected_rst": sorted(affected_rst),
        "matched_sources": matched_sources,
        "unmatched_files": unmatched_files,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze webui changes for docs impact"
    )
    parser.add_argument(
        "--mapping",
        default=".github/docs-mapping.yml",
        help="Path to docs-mapping.yml (default: .github/docs-mapping.yml)",
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Changed files (reads from stdin if not provided)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    if args.files:
        changed_files = args.files
    else:
        changed_files = [line.strip() for line in sys.stdin if line.strip()]

    # Filter to react/src/ files only
    changed_files = [f for f in changed_files if f.startswith("react/src/")]

    if not changed_files:
        if args.format == "json":
            print(
                json.dumps(
                    {"affected_rst": [], "matched_sources": {}, "unmatched_files": []}
                )
            )
        else:
            print("No react/src/ files in changed list. Nothing to do.")
        sys.exit(0)

    try:
        mapping = load_mapping(args.mapping)
    except Exception as e:
        print(f"Error loading mapping file: {e}", file=sys.stderr)
        sys.exit(1)

    result = find_affected_docs(changed_files, mapping)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Changed webui files: {len(changed_files)}")
        print(f"Affected RST docs:   {len(result['affected_rst'])}")
        print()
        if result["affected_rst"]:
            print("RST files that need updating:")
            for rst in result["affected_rst"]:
                print(f"  - docs/{rst}")
        if result["unmatched_files"]:
            print(f"\nUnmatched files ({len(result['unmatched_files'])}):")
            for f in result["unmatched_files"]:
                print(f"  - {f}")

    sys.exit(0)


if __name__ == "__main__":
    main()
