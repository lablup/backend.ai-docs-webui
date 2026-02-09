#!/usr/bin/env python3
"""
Generate a detailed Draft PR body for documentation updates.

Reads analysis results and changed source files to produce a Markdown summary
that helps a reviewer (using Claude Code CLI) update the RST docs efficiently.
"""

import argparse
import json
import sys
from pathlib import Path


def get_file_summary(filepath: Path, max_lines: int = 50) -> str:
    """Get a truncated preview of a file's content."""
    if not filepath.exists():
        return "(file not found)"
    lines = filepath.read_text().splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines)"


def get_exports_and_components(filepath: Path) -> list:
    """Extract exported component/function names from a TSX file."""
    if not filepath.exists():
        return []
    content = filepath.read_text()
    exports = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("export default "):
            name = line.replace("export default ", "").split("(")[0].split("{")[0].strip().rstrip(";")
            if name and name != "function":
                exports.append(name)
        elif line.startswith("export const ") or line.startswith("export function "):
            parts = line.split()
            if len(parts) >= 3:
                name = parts[2].split("(")[0].split(":")[0].split("<")[0]
                exports.append(name)
    return exports


def main():
    parser = argparse.ArgumentParser(description="Generate PR summary")
    parser.add_argument("--analysis", required=True, help="Path to analysis.json")
    parser.add_argument("--changed-files", required=True, help="Comma-separated changed files")
    parser.add_argument("--webui-path", required=True, help="Path to webui checkout")
    parser.add_argument("--docs-path", required=True, help="Path to docs directory")
    parser.add_argument("--release-tag", required=True, help="Release tag")
    parser.add_argument("--release-url", required=True, help="Release URL")
    args = parser.parse_args()

    with open(args.analysis) as f:
        analysis = json.load(f)

    webui_path = Path(args.webui_path)
    docs_path = Path(args.docs_path)
    changed_files = [f.strip() for f in args.changed_files.split(",") if f.strip()]
    affected_rst = analysis.get("affected_rst", [])
    matched = analysis.get("matched_sources", {})

    # --- Build PR body ---
    lines = [
        f"## Documentation Update for WebUI {args.release_tag}",
        "",
        f"**Release**: {args.release_url}",
        f"**Changed source files**: {len(changed_files)}",
        f"**Affected RST files**: {len(affected_rst)}",
        "",
        "---",
        "",
        "## How to Update",
        "",
        "1. Check out this branch locally",
        "2. Run Claude Code CLI in the repo root:",
        "   ```",
        f'   claude "이 PR은 webui {args.release_tag} 릴리즈에 따른 문서 업데이트입니다.',
        "   아래 '변경된 소스 파일' 섹션을 참고해서 영향받는 RST 파일을 업데이트해 주세요.",
        '   CLAUDE.md와 STYLE_GUIDE.md의 규칙을 따라주세요."',
        "   ```",
        "",
        "---",
        "",
        "## Affected RST Files",
        "",
    ]

    for rst in affected_rst:
        rst_path = docs_path / rst
        line_count = len(rst_path.read_text().splitlines()) if rst_path.exists() else 0
        lines.append(f"- `docs/{rst}` ({line_count} lines)")

    lines.extend(["", "---", "", "## Changed Source Files", ""])

    # Group changed files by their matched RST docs
    rst_to_sources = {}
    for src_file, matches in matched.items():
        for match in matches:
            if match["type"] == "page":
                key = match["route"]
            else:
                key = match["name"]
            rst_to_sources.setdefault(key, []).append(src_file)

    for group_key, sources in sorted(rst_to_sources.items()):
        lines.append(f"### `{group_key}`")
        lines.append("")
        for src in sources:
            src_path = webui_path / src
            exports = get_exports_and_components(src_path)
            export_str = f" (exports: {', '.join(exports)})" if exports else ""
            line_count = len(src_path.read_text().splitlines()) if src_path.exists() else 0
            lines.append(f"- `{src}` ({line_count} lines){export_str}")
        lines.append("")

    # Unmatched files
    unmatched = analysis.get("unmatched_files", [])
    if unmatched:
        lines.extend(["### Unmatched (no RST mapping)", ""])
        for f in unmatched:
            lines.append(f"- `{f}`")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## Review Checklist",
        "",
        "- [ ] RST 파일 업데이트 완료",
        "- [ ] 스크린샷 확인/업데이트",
        "- [ ] `make html` 빌드 확인",
        "- [ ] 번역 싱크 필요 여부 확인",
        "",
        "---",
        f"*Auto-generated for webui {args.release_tag} release.*",
    ])

    print("\n".join(lines))


if __name__ == "__main__":
    main()
