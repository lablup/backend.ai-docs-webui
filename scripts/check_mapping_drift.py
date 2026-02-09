#!/usr/bin/env python3
"""
Check docs-mapping.yml for drift against actual webui pages and docs RST files.

Detects:
  1. unmapped_page: Page in webui with no mapping entry
  2. stale_source: Mapping references a source file that doesn't exist
  3. stale_rst: Mapping references an RST file that doesn't exist
  4. orphaned_rst: RST file not referenced in any mapping entry
"""

import argparse
import os
import sys
from pathlib import Path

import yaml

# Page files to skip (not user-facing documentation targets)
SKIP_PAGES = {"Page401.tsx", "Page404.tsx"}

# RST files that are structural and don't need source mapping
STRUCTURAL_RST = {
    "index.rst",
    "disclaimer.rst",
    "quickstart.rst",
    "license_agreement/license_agreement.rst",
    "references/references.rst",
    "installation/installation.rst",
    "overview/overview.rst",
    "trouble_shooting/trouble_shooting.rst",
    "appendix/appendix.rst",
    "appendix/allocate_gpu.rst",
    "appendix/resource_and_scheduler.rst",
}


def main():
    parser = argparse.ArgumentParser(description="Check mapping drift")
    parser.add_argument("--mapping", required=True, help="Path to docs-mapping.yml")
    parser.add_argument("--webui-path", required=True, help="Path to webui checkout")
    parser.add_argument("--docs-path", required=True, help="Path to docs directory")
    args = parser.parse_args()

    with open(args.mapping) as f:
        mapping = yaml.safe_load(f)

    webui_path = Path(args.webui_path)
    docs_path = Path(args.docs_path)
    issues = []

    # 1. Find all page files in webui
    actual_pages = set()
    pages_dir = webui_path / "react" / "src" / "pages"
    if pages_dir.exists():
        for f in pages_dir.glob("*.tsx"):
            if f.name not in SKIP_PAGES:
                actual_pages.add(f"react/src/pages/{f.name}")

    # 2. Collect all source patterns from mapping
    mapped_sources = set()
    for entry in mapping.get("pages", []):
        for src in entry.get("sources", []):
            mapped_sources.add(src)

    # 3. Unmapped pages
    for page in sorted(actual_pages):
        if page not in mapped_sources:
            issues.append(
                {
                    "type": "unmapped_page",
                    "severity": "warning",
                    "message": f"Page `{page}` exists in webui but has no mapping entry",
                }
            )

    # 4. Stale source references
    for entry in mapping.get("pages", []):
        for src in entry.get("sources", []):
            if "**" not in src and not (webui_path / src).exists():
                issues.append(
                    {
                        "type": "stale_source",
                        "severity": "error",
                        "message": f"Mapping references `{src}` but file does not exist (route: {entry.get('route')})",
                    }
                )

    # 5. Stale RST references
    all_mapped_rst = set()
    for entry in mapping.get("pages", []) + mapping.get("components", []):
        for doc in entry.get("docs", []):
            all_mapped_rst.add(doc)
            if not (docs_path / doc).exists():
                issues.append(
                    {
                        "type": "stale_rst",
                        "severity": "error",
                        "message": f"Mapping references `docs/{doc}` but RST file does not exist",
                    }
                )

    # 6. Orphaned RST files
    actual_rst = set()
    for rst_file in docs_path.rglob("*.rst"):
        rel = str(rst_file.relative_to(docs_path))
        if rel.startswith("locale/"):
            continue
        actual_rst.add(rel)

    for rst in sorted(actual_rst - all_mapped_rst - STRUCTURAL_RST):
        issues.append(
            {
                "type": "orphaned_rst",
                "severity": "info",
                "message": f"RST file `docs/{rst}` is not referenced in any mapping entry",
            }
        )

    # GitHub Actions output
    has_drift = any(i["severity"] in ("warning", "error") for i in issues)
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"has_drift={'true' if has_drift else 'false'}\n")

    # Console output
    if not issues:
        print("No drift detected. Mapping is up to date.")
    else:
        print(f"Drift check found {len(issues)} issue(s):\n")
        for issue in issues:
            icon = {"error": "ERROR", "warning": "WARN", "info": "INFO"}[
                issue["severity"]
            ]
            print(f"  [{icon}] {issue['message']}")

    # Markdown report for GitHub issue
    with open("/tmp/drift_report.md", "w") as f:
        f.write("## Docs Mapping Drift Report\n\n")
        if not issues:
            f.write("No drift detected. All mappings are current.\n")
        else:
            for severity, label in [
                ("error", "Errors (must fix)"),
                ("warning", "Warnings (should investigate)"),
                ("info", "Info"),
            ]:
                items = [i for i in issues if i["severity"] == severity]
                if items:
                    f.write(f"### {label}\n")
                    for i in items:
                        f.write(f"- {i['message']}\n")
                    f.write("\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
