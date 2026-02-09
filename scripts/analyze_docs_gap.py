#!/usr/bin/env python3
"""
Analyze documentation gaps between webui releases and docs-webui.

Compares webui code changes between two release tags and checks which
features are missing or outdated in the current RST documentation.

Usage:
  # Compare between two specific tags:
  python scripts/analyze_docs_gap.py --from v25.19.2 --to v26.1.0

  # Compare latest two releases (auto-detect):
  python scripts/analyze_docs_gap.py

  # With custom paths:
  python scripts/analyze_docs_gap.py --webui-path /path/to/webui --docs-path docs

  # Output as JSON:
  python scripts/analyze_docs_gap.py --format json

  # Output as markdown (for PR / issue body):
  python scripts/analyze_docs_gap.py --format markdown > gap_report.md

  # Output as actionable summary grouped by RST file (priority order):
  python scripts/analyze_docs_gap.py --format summary > update_plan.md
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

# Generic words that appear everywhere in docs and should not count as coverage
STOPWORDS = {
    "with", "from", "into", "that", "this", "implement", "feature", "add",
    "react", "enhance", "improve", "support", "update", "create", "display",
    "handling", "using", "based", "better", "more", "migration", "migrate",
    "component", "page", "modal", "form", "list", "table", "button", "select",
    "setting", "item", "view", "panel", "content", "options", "data", "type",
    "state", "management", "error", "loading", "default", "custom", "query",
    "user", "session", "agent", "folder", "model", "image", "resource",
    "group", "project", "endpoint", "service",
}


def build_search_terms(commit_msg: str, files: list) -> list:
    """Extract feature-specific search terms from commit message and file names.

    Uses compound phrases from the commit message and distinctive component
    names to avoid matching on generic words like 'user' or 'session'.
    """
    terms = []

    # From commit message: extract the feature description as compound phrases
    msg_clean = re.sub(r"feat\([^)]+\):\s*", "", commit_msg)
    msg_clean = re.sub(r"\(#\d+\)", "", msg_clean).strip().lower()

    # Add 2-3 word compound phrases (more distinctive than single words)
    words = re.split(r"[\s/\-_]+", msg_clean)
    words = [w for w in words if w and w not in STOPWORDS]
    for i in range(len(words)):
        if len(words[i]) > 3 and words[i] not in STOPWORDS:
            terms.append(words[i])
        # bigrams
        if i + 1 < len(words):
            bigram = f"{words[i]} {words[i+1]}"
            if len(bigram) > 8:
                terms.append(bigram)

    # From file names: use full component names (CamelCase → "space separated lower")
    for f in files:
        name = Path(f).stem
        # Convert CamelCase to phrase: "BulkUserUpdateModal" → "bulk user update modal"
        parts = re.findall(r"[A-Z][a-z]+|[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)", name)
        if len(parts) >= 2:
            full_name = " ".join(p.lower() for p in parts)
            # Remove generic suffixes for matching
            for suffix in ("modal", "drawer", "content", "page", "button", "list", "form", "items"):
                full_name = re.sub(rf"\s*{suffix}$", "", full_name)
            if len(full_name) > 5:
                terms.append(full_name)

    return list(set(terms))


def run_git(args: list, cwd: str) -> str:
    result = subprocess.run(
        ["git"] + args, capture_output=True, text=True, cwd=cwd
    )
    return result.stdout.strip()


def get_release_tags(webui_path: str) -> list:
    """Get sorted list of non-prerelease tags."""
    tags = run_git(["tag", "--sort=-creatordate"], webui_path)
    return [t for t in tags.splitlines() if re.match(r"^v\d+\.\d+\.\d+$", t)]


def get_feature_commits(webui_path: str, from_tag: str, to_tag: str) -> list:
    """Get feature commits between two tags."""
    log = run_git(
        ["log", "--oneline", f"{from_tag}..{to_tag}", "--", "react/src/"],
        webui_path,
    )
    commits = []
    for line in log.splitlines():
        if not line.strip():
            continue
        sha = line.split()[0]
        msg = line[len(sha) :].strip()
        is_feat = "feat(" in msg or "feat:" in msg
        commits.append({"sha": sha, "message": msg, "is_feature": is_feat})
    return commits


def get_changed_files_for_commit(webui_path: str, sha: str) -> list:
    """Get files changed in a specific commit."""
    output = run_git(
        ["diff-tree", "--no-commit-id", "-r", "--name-only", sha], webui_path
    )
    return [f for f in output.splitlines() if f.startswith("react/src/")]


def get_all_changed_files(webui_path: str, from_tag: str, to_tag: str) -> list:
    """Get all changed react/src/ files between two tags."""
    output = run_git(
        ["diff", "--name-only", f"{from_tag}..{to_tag}", "--", "react/src/"],
        webui_path,
    )
    return [f for f in output.splitlines() if f.strip()]


def search_in_rst(docs_path: str, rst_file: str, terms: list) -> dict:
    """Search for terms in an RST file. Returns match count per term."""
    rst_path = Path(docs_path) / rst_file
    if not rst_path.exists():
        return {}
    content = rst_path.read_text().lower()
    return {term: content.count(term) for term in terms if content.count(term) > 0}


def analyze_feature_gap(
    feature: dict, webui_path: str, docs_path: str, mapping: dict
) -> dict:
    """Analyze whether a feature commit is reflected in docs."""
    sha = feature["sha"]
    msg = feature["message"]
    changed_files = get_changed_files_for_commit(webui_path, sha)

    # Find affected RST files via mapping
    affected_rst = set()
    for entry in mapping.get("pages", []) + mapping.get("components", []):
        sources = entry.get("sources", [])
        docs = entry.get("docs", [])
        for src_pattern in sources:
            if "**" in src_pattern:
                base = src_pattern.replace("/**", "")
                matches = [f for f in changed_files if f.startswith(base + "/")]
            else:
                matches = [f for f in changed_files if f == src_pattern]
            if matches:
                affected_rst.update(docs)

    # Build search terms and check docs
    terms = build_search_terms(msg, changed_files)
    doc_coverage = {}
    for rst in affected_rst:
        found = search_in_rst(docs_path, rst, terms)
        doc_coverage[rst] = {
            "found_terms": found,
            "coverage_score": len(found) / max(len(terms), 1),
        }

    # Determine gap level
    if not affected_rst:
        gap_level = "no_mapping"
    elif all(v["coverage_score"] >= 0.3 for v in doc_coverage.values()):
        gap_level = "likely_documented"
    elif any(v["coverage_score"] > 0 for v in doc_coverage.values()):
        gap_level = "partially_documented"
    else:
        gap_level = "not_documented"

    return {
        "sha": sha,
        "message": msg,
        "changed_files": changed_files,
        "affected_rst": sorted(affected_rst),
        "search_terms": terms,
        "doc_coverage": doc_coverage,
        "gap_level": gap_level,
    }


def format_text(report: dict) -> str:
    lines = []
    lines.append(f"=== Docs Gap Analysis: {report['from_tag']} → {report['to_tag']} ===")
    lines.append(f"Total commits: {report['total_commits']} ({report['feature_commits']} features)")
    lines.append(f"Changed files: {report['changed_files_count']}")
    lines.append(f"Affected RST:  {len(report['affected_rst'])}")
    lines.append("")

    for level, label in [
        ("not_documented", "NOT DOCUMENTED (needs update)"),
        ("partially_documented", "PARTIALLY DOCUMENTED (may need update)"),
        ("no_mapping", "NO RST MAPPING (no docs target)"),
    ]:
        features = [f for f in report["features"] if f["gap_level"] == level]
        if not features:
            continue
        lines.append(f"--- {label} ({len(features)}) ---")
        for f in features:
            lines.append(f"  [{f['sha'][:7]}] {f['message']}")
            if f["affected_rst"]:
                lines.append(f"    RST: {', '.join(f['affected_rst'])}")
            lines.append(f"    Files: {len(f['changed_files'])} changed")
        lines.append("")

    documented = [f for f in report["features"] if f["gap_level"] == "likely_documented"]
    if documented:
        lines.append(f"--- LIKELY DOCUMENTED ({len(documented)}) ---")
        for f in documented:
            lines.append(f"  [{f['sha'][:7]}] {f['message']}")
        lines.append("")

    return "\n".join(lines)


def format_markdown(report: dict) -> str:
    lines = []
    lines.append(f"# Docs Gap Analysis: {report['from_tag']} → {report['to_tag']}")
    lines.append("")
    lines.append(f"- **Total commits**: {report['total_commits']} ({report['feature_commits']} features)")
    lines.append(f"- **Changed files**: {report['changed_files_count']}")
    lines.append(f"- **Affected RST files**: {len(report['affected_rst'])}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for level, label, emoji in [
        ("not_documented", "Not Documented", "🔴"),
        ("partially_documented", "Partially Documented", "🟡"),
        ("no_mapping", "No RST Mapping", "⚪"),
    ]:
        features = [f for f in report["features"] if f["gap_level"] == level]
        if not features:
            continue
        lines.append(f"## {emoji} {label} ({len(features)})")
        lines.append("")
        for f in features:
            lines.append(f"### `{f['sha'][:7]}` {f['message']}")
            if f["affected_rst"]:
                lines.append(f"- **RST files**: {', '.join(f'`{r}`' for r in f['affected_rst'])}")
            if f["changed_files"]:
                page_files = [p for p in f["changed_files"] if "/pages/" in p]
                comp_files = [p for p in f["changed_files"] if "/components/" in p]
                if page_files:
                    lines.append(f"- **Pages**: {', '.join(f'`{Path(p).name}`' for p in page_files)}")
                if comp_files:
                    lines.append(f"- **Components**: {', '.join(f'`{Path(p).name}`' for p in comp_files[:5])}" +
                                 (f" +{len(comp_files)-5} more" if len(comp_files) > 5 else ""))
            lines.append("")

    documented = [f for f in report["features"] if f["gap_level"] == "likely_documented"]
    if documented:
        lines.append(f"## ✅ Likely Documented ({len(documented)})")
        lines.append("")
        for f in documented:
            lines.append(f"- `{f['sha'][:7]}` {f['message']}")
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated by `scripts/analyze_docs_gap.py`*")
    return "\n".join(lines)


def extract_feature_description(msg: str) -> str:
    """Extract clean feature description from commit message."""
    clean = re.sub(r"feat\([^)]+\):\s*", "", msg)
    clean = re.sub(r"\s*\(#\d+\)", "", clean).strip()
    return clean


# Patterns in commit messages that indicate internal/infrastructure changes
# (no user-visible UI change, so docs update is not needed).
INTERNAL_PATTERNS = [
    r"(?i)add\s+data.testid",
    r"(?i)BAILogger|replace.*with\s+console",
    r"(?i)migrate.*(?:nuqs|query.params|URL\s+state\s+management)",
    r"(?i)upgrade.*SDK|SDK.*v\d",
    r"(?i)CSS.based\s+ellipsis|Safari\s+compatibility",
    r"(?i)usePaginationFragment",
    r"(?i)clamp\s+CPU.*stats",
    r"(?i)i18n\s+translations?\s+of",
    r"(?i)replace\s+all\w+V2\s+to",
    r"(?i)Relay\s+Subscription\s+for",
    r"(?i)async\s+file\s+deletion\s+api",
]


def is_internal_change(feature: dict) -> bool:
    """Heuristic: detect internal/infrastructure changes that don't need docs."""
    msg = feature["message"]
    for pattern in INTERNAL_PATTERNS:
        if re.search(pattern, msg):
            return True
    return False


def format_summary(report: dict) -> str:
    """Generate an actionable documentation update plan grouped by RST file."""
    features = report["features"]

    # Classify features
    internal = []
    no_mapping = []
    likely_documented = []
    needs_update = []  # not_documented + partially_documented

    for f in features:
        if f["gap_level"] == "likely_documented":
            likely_documented.append(f)
        elif f["gap_level"] == "no_mapping":
            no_mapping.append(f)
        elif is_internal_change(f):
            internal.append(f)
        else:
            needs_update.append(f)

    # Group needs_update features by RST file
    rst_features: dict[str, list] = {}
    for f in needs_update:
        for rst in f["affected_rst"]:
            rst_features.setdefault(rst, []).append(f)

    # Sort RST files by feature count (descending = highest priority first)
    sorted_rst = sorted(rst_features.items(), key=lambda x: len(x[1]), reverse=True)

    # --- Build output ---
    lines = []
    lines.append(f"# Documentation Update Plan: {report['from_tag']} → {report['to_tag']}")
    lines.append("")

    not_doc_count = len([f for f in needs_update if f["gap_level"] == "not_documented"])
    partial_count = len([f for f in needs_update if f["gap_level"] == "partially_documented"])

    lines.append("## Overview")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|----------|-------|")
    lines.append(f"| Total feature commits | {report['feature_commits']} |")
    lines.append(f"| Not documented | {not_doc_count} |")
    lines.append(f"| Partially documented | {partial_count} |")
    lines.append(f"| No RST mapping | {len(no_mapping)} |")
    lines.append(f"| Internal (no doc needed) | {len(internal)} |")
    lines.append(f"| Likely documented | {len(likely_documented)} |")
    lines.append(f"| RST files to update | {len(sorted_rst)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Per-RST-file sections
    for priority, (rst, rst_feats) in enumerate(sorted_rst, 1):
        # Deduplicate (same feature appears via multiple RST mappings)
        seen = set()
        unique = []
        for f in rst_feats:
            if f["sha"] not in seen:
                seen.add(f["sha"])
                unique.append(f)

        not_doc = [f for f in unique if f["gap_level"] == "not_documented"]
        partial = [f for f in unique if f["gap_level"] == "partially_documented"]

        lines.append(f"## Priority {priority}: `docs/{rst}` ({len(unique)} features)")
        lines.append("")

        if not_doc:
            lines.append(f"**Not documented ({len(not_doc)})** — new content required:")
            lines.append("")
            for f in not_doc:
                desc = extract_feature_description(f["message"])
                page_files = [p for p in f["changed_files"] if "/pages/" in p]
                page_str = ""
                if page_files:
                    page_str = " | Pages: " + ", ".join(f"`{Path(p).name}`" for p in page_files)
                lines.append(f"- `{f['sha'][:7]}` {desc}{page_str}")
            lines.append("")

        if partial:
            lines.append(f"**Partially documented ({len(partial)})** — update/supplement needed:")
            lines.append("")
            for f in partial:
                desc = extract_feature_description(f["message"])
                page_files = [p for p in f["changed_files"] if "/pages/" in p]
                page_str = ""
                if page_files:
                    page_str = " | Pages: " + ", ".join(f"`{Path(p).name}`" for p in page_files)
                lines.append(f"- `{f['sha'][:7]}` {desc}{page_str}")
            lines.append("")

    # No RST Mapping
    if no_mapping:
        lines.append("---")
        lines.append("")
        lines.append(f"## No RST Mapping ({len(no_mapping)} features)")
        lines.append("")
        lines.append("These features have no corresponding RST file. "
                      "Consider adding to an existing doc or creating a new one.")
        lines.append("")
        for f in no_mapping:
            desc = extract_feature_description(f["message"])
            comp_files = [p for p in f["changed_files"]
                          if "/components/" in p or "/pages/" in p]
            file_str = ""
            if comp_files:
                file_str = " | " + ", ".join(f"`{Path(p).name}`" for p in comp_files[:4])
                if len(comp_files) > 4:
                    file_str += f" +{len(comp_files) - 4} more"
            lines.append(f"- `{f['sha'][:7]}` {desc}{file_str}")
        lines.append("")

    # Internal changes (skipped)
    if internal:
        lines.append("---")
        lines.append("")
        lines.append(f"## Internal Changes — No Doc Update Needed ({len(internal)})")
        lines.append("")
        lines.append("Infrastructure, refactoring, or internal migration with no user-facing UI change.")
        lines.append("")
        for f in internal:
            desc = extract_feature_description(f["message"])
            lines.append(f"- ~~`{f['sha'][:7]}` {desc}~~")
        lines.append("")

    # Likely documented
    if likely_documented:
        lines.append("---")
        lines.append("")
        lines.append(f"## Likely Documented ({len(likely_documented)} features)")
        lines.append("")
        lines.append("These features appear to already have documentation coverage. Verify during review.")
        lines.append("")
        for f in likely_documented:
            desc = extract_feature_description(f["message"])
            lines.append(f"- `{f['sha'][:7]}` {desc}")
        lines.append("")

    lines.append("---")
    lines.append(f"*Generated by `scripts/analyze_docs_gap.py --format summary`*")
    return "\n".join(lines)


def format_json(report: dict) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Analyze docs gap between webui releases")
    parser.add_argument("--from", dest="from_tag", help="Starting release tag (default: auto-detect previous)")
    parser.add_argument("--to", dest="to_tag", help="Ending release tag (default: auto-detect latest)")
    parser.add_argument("--webui-path", default="../webui", help="Path to webui repo (default: ../webui)")
    parser.add_argument("--docs-path", default="docs", help="Path to docs directory (default: docs)")
    parser.add_argument("--mapping", default=".github/docs-mapping.yml", help="Path to docs-mapping.yml")
    parser.add_argument("--format", choices=["text", "markdown", "json", "summary"], default="text", help="Output format")
    args = parser.parse_args()

    webui_path = str(Path(args.webui_path).resolve())
    docs_path = str(Path(args.docs_path).resolve())

    # Auto-detect tags if not specified
    tags = get_release_tags(webui_path)
    if not tags:
        print("Error: No release tags found in webui repo.", file=sys.stderr)
        sys.exit(1)

    to_tag = args.to_tag or tags[0]
    from_tag = args.from_tag
    if not from_tag:
        try:
            idx = tags.index(to_tag)
            from_tag = tags[idx + 1] if idx + 1 < len(tags) else tags[-1]
        except ValueError:
            from_tag = tags[1] if len(tags) > 1 else tags[0]

    print(f"Analyzing: {from_tag} → {to_tag}", file=sys.stderr)

    # Load mapping
    with open(args.mapping) as f:
        mapping = yaml.safe_load(f)

    # Get commits and changed files
    commits = get_feature_commits(webui_path, from_tag, to_tag)
    feature_commits = [c for c in commits if c["is_feature"]]
    all_changed = get_all_changed_files(webui_path, from_tag, to_tag)

    # Run analyze_changes for overall affected RST list
    from analyze_changes import find_affected_docs, load_mapping as load_map
    mapping_data = load_map(args.mapping)
    overall = find_affected_docs(all_changed, mapping_data)

    # Analyze each feature commit
    features = []
    for feat in feature_commits:
        gap = analyze_feature_gap(feat, webui_path, docs_path, mapping)
        features.append(gap)

    # Sort: not_documented first, then partially, then no_mapping, then documented
    priority = {"not_documented": 0, "partially_documented": 1, "no_mapping": 2, "likely_documented": 3}
    features.sort(key=lambda f: priority.get(f["gap_level"], 99))

    report = {
        "from_tag": from_tag,
        "to_tag": to_tag,
        "total_commits": len(commits),
        "feature_commits": len(feature_commits),
        "changed_files_count": len(all_changed),
        "affected_rst": overall["affected_rst"],
        "features": features,
    }

    if args.format == "json":
        print(format_json(report))
    elif args.format == "markdown":
        print(format_markdown(report))
    elif args.format == "summary":
        print(format_summary(report))
    else:
        print(format_text(report))


if __name__ == "__main__":
    # Add scripts/ to path for analyze_changes import
    sys.path.insert(0, str(Path(__file__).parent))
    main()
