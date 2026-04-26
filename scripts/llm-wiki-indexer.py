#!/usr/bin/env python3
"""Scan an Obsidian LLM Wiki vault and produce retrieval/index health artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_VAULT = Path(os.environ.get("LLM_WIKI_VAULT", "~/Obsidian/LLM-Wiki")).expanduser()
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".heic", ".bmp"}
ATTACHMENT_EXTS = IMAGE_EXTS | {".pdf", ".docx", ".xlsx", ".pptx", ".zip"}
SENSITIVE_PARTS = {"账号", "激活", "权限申请", "系统"}
INDEX_PREFIX = "00-索引/"
WIKILINK_RE = re.compile(r"\[\[([^\]#|]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


@dataclass
class ScanScope:
    name: str
    roots: list[Path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan an Obsidian LLM Wiki vault.")
    parser.add_argument("--vault", default=str(DEFAULT_VAULT), help="Vault root path.")
    parser.add_argument(
        "--scope",
        choices=["markitdown-input", "all"],
        default="markitdown-input",
        help="Report scope. Map generation always covers the whole vault.",
    )
    parser.add_argument("--map-out", default=None, help="Machine-readable JSON map output.")
    parser.add_argument("--report-out", default=None, help="Human-readable Markdown report output.")
    parser.add_argument("--open-report", action="store_true", help="Open report with Obsidian CLI when possible.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def strip_code_fences(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def parse_frontmatter(text: str) -> dict[str, Any]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, Any] = {}
    current_key = None
    for raw in match.group(1).splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip())
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                data[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                data[key] = [item.strip() for item in inner.split(",") if item.strip()]
            else:
                data[key] = value
    return data


def title_from(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def summary_from(text: str) -> str:
    clean = FRONTMATTER_RE.sub("", text, count=1)
    clean = strip_code_fences(clean)
    lines = []
    capture = False
    for line in clean.splitlines():
        stripped = line.strip()
        if stripped in {"## 摘要", "## Summary"}:
            capture = True
            continue
        if capture and stripped.startswith("## "):
            break
        if capture and stripped and not stripped.startswith("#"):
            lines.append(stripped.lstrip("- "))
        if len(" ".join(lines)) > 160:
            break
    if not lines:
        for line in clean.splitlines():
            stripped = line.strip()
            if stripped and not stripped.startswith("#") and not stripped.startswith("|"):
                lines.append(stripped.lstrip("- "))
            if len(" ".join(lines)) > 160:
                break
    return " ".join(lines)[:220]


def keywords_from(path: Path, fm: dict[str, Any], title: str) -> list[str]:
    parts = [title]
    parts.extend(path.with_suffix("").parts)
    for key in ("标签", "tags", "别名", "aliases"):
        value = fm.get(key)
        if isinstance(value, list):
            parts.extend(str(v) for v in value)
        elif value:
            parts.append(str(value))
    seen: set[str] = set()
    words: list[str] = []
    for item in parts:
        for token in re.split(r"[/\s,，、|｜\-_.()（）【】\[\]]+", item):
            token = token.strip()
            if len(token) >= 2 and token not in seen:
                seen.add(token)
                words.append(token)
    return words[:20]


def iter_markdown(root: Path) -> list[Path]:
    ignored = {".obsidian", ".claude", ".claudian", ".git"}
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignored and not d.startswith(".")]
        for filename in filenames:
            if filename.endswith(".md"):
                result.append(Path(dirpath) / filename)
    return sorted(result)


def obsidian_status() -> dict[str, Any]:
    cmd = shutil.which("obsidian") or shutil.which("obsidian-cli")
    running = False
    try:
        proc = subprocess.run(["pgrep", "-x", "Obsidian"], capture_output=True, text=True, timeout=2)
        running = proc.returncode == 0
    except Exception:
        running = False
    return {"command": cmd, "running": running}


def build_map(vault: Path) -> tuple[dict[str, Any], dict[str, list[str]]]:
    files = iter_markdown(vault)
    note_paths = {rel(p, vault).removesuffix(".md") for p in files}
    note_titles = {p.stem for p in files}
    indexed_targets: set[str] = set()
    notes: list[dict[str, Any]] = []
    broken: list[str] = []

    for path in files:
        note_rel = rel(path, vault)
        text = read_text(path)
        fm = parse_frontmatter(text)
        title = title_from(text, path)
        body_for_links = strip_code_fences(text)
        links = []
        attachment_links = []
        for match in WIKILINK_RE.finditer(body_for_links):
            target = match.group(1).strip().removesuffix(".md")
            if Path(target).suffix.lower() in ATTACHMENT_EXTS:
                attachment_links.append(target)
                continue
            links.append(target)
            if note_rel != "99-收件箱/每日整理候选.md":
                indexed_targets.add(target)
            if target not in note_paths and target not in note_titles:
                broken.append(f"{rel(path, vault)} -> {target}")

        parts = set(Path(note_rel).parts)
        sensitive = bool(parts & SENSITIVE_PARTS)
        notes.append(
            {
                "path": note_rel,
                "title": title,
                "folder": Path(note_rel).parent.as_posix(),
                "type": fm.get("类型") or fm.get("type") or "",
                "status": fm.get("状态") or fm.get("status") or "",
                "tags": fm.get("标签") or fm.get("tags") or [],
                "aliases": fm.get("别名") or fm.get("aliases") or [],
                "updated": fm.get("更新") or fm.get("updated") or "",
                "links": sorted(set(links)),
                "attachment_links": sorted(set(attachment_links)),
                "keywords": keywords_from(Path(note_rel), fm, title),
                "summary": "" if sensitive else summary_from(text),
                "has_frontmatter": bool(fm),
                "has_purpose": "## 用途" in text,
                "is_index": note_rel.startswith(INDEX_PREFIX),
                "is_sensitive_path": sensitive,
            }
        )

    indexed_paths = {target for target in indexed_targets if target in note_paths}
    title_to_paths: dict[str, list[str]] = {}
    for note in notes:
        title_to_paths.setdefault(note["title"], []).append(note["path"])

    orphan_notes = [
        n["path"]
        for n in notes
        if not n["is_index"] and n["path"].removesuffix(".md") not in indexed_paths
    ]
    missing_purpose = [n["path"] for n in notes if not n["is_index"] and not n["has_purpose"]]
    duplicate_titles = {
        title: paths for title, paths in title_to_paths.items() if len(paths) > 1
    }

    project_dirs: dict[str, list[str]] = {}
    for n in notes:
        folder = n["folder"]
        if folder in {".", "00-索引"}:
            continue
        project_dirs.setdefault(folder, []).append(n["path"])
    suspected_projects = {
        folder: paths
        for folder, paths in project_dirs.items()
        if len(paths) >= 2 and not any(Path(p).name in {"项目索引.md", "说明.md"} for p in paths)
    }

    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "vault": str(vault),
        "obsidian_cli": obsidian_status(),
        "counts": {
            "markdown_files": len(files),
            "broken_wikilinks": len(broken),
            "orphan_notes": len(orphan_notes),
            "missing_purpose": len(missing_purpose),
            "duplicate_titles": len(duplicate_titles),
            "suspected_project_dirs": len(suspected_projects),
        },
        "notes": notes,
    }
    health = {
        "broken": broken,
        "orphan_notes": orphan_notes,
        "missing_purpose": missing_purpose,
        "duplicate_titles": [f"{k}: {', '.join(v)}" for k, v in duplicate_titles.items()],
        "suspected_projects": [f"{k}: {', '.join(v)}" for k, v in suspected_projects.items()],
    }
    return data, health


def scope_for(vault: Path, name: str) -> ScanScope:
    if name == "all":
        return ScanScope("all", [vault])
    return ScanScope("markitdown-input", [vault / "markitdown-input"])


def in_roots(note_path: str, roots: list[Path], vault: Path) -> bool:
    abs_path = vault / note_path
    for root in roots:
        try:
            abs_path.relative_to(root)
            return True
        except ValueError:
            continue
    return False


def write_report(report_path: Path, data: dict[str, Any], health: dict[str, list[str]], scope: ScanScope) -> None:
    vault = Path(data["vault"])
    scoped_notes = [n for n in data["notes"] if in_roots(n["path"], scope.roots, vault)]
    recent_or_scoped = scoped_notes if scope.name != "all" else data["notes"]
    cli = data["obsidian_cli"]
    lines = [
        "---",
        "类型: 整理报告",
        "状态: 草稿",
        "标签:",
        "  - LLM/wiki",
        "  - 自动整理",
        f"更新: {datetime.now().strftime('%Y-%m-%d')}",
        "---",
        "",
        "# 每日整理候选",
        "",
        f"- 生成时间：{data['generated_at']}",
        f"- 扫描范围：`{scope.name}`",
        f"- Vault：`{data['vault']}`",
        f"- Obsidian CLI：`{cli.get('command') or '未找到'}`",
        f"- Obsidian 是否运行：{'是' if cli.get('running') else '否'}",
        "",
        "## 总览",
        "",
    ]
    for key, value in data["counts"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## 本次范围内文件", ""])
    if recent_or_scoped:
        for note in recent_or_scoped:
            sensitive = "，敏感路径，仅路径级索引" if note["is_sensitive_path"] else ""
            lines.append(f"- [[{note['path'].removesuffix('.md')}]] - {note['title']}{sensitive}")
    else:
        lines.append("- 未发现范围内 Markdown 文件。")

    sections = [
        ("坏链", health["broken"]),
        ("缺少索引入口的笔记", health["orphan_notes"]),
        ("缺少用途段的笔记", health["missing_purpose"]),
        ("重复标题", health["duplicate_titles"]),
        ("疑似项目目录", health["suspected_projects"]),
    ]
    for title, items in sections:
        lines.extend(["", f"## {title}", ""])
        filtered = items
        if scope.name != "all" and title not in {"重复标题"}:
            filtered = [item for item in items if any(root.as_posix() in str(vault / item.split(" -> ")[0]) for root in scope.roots)]
        if filtered:
            for item in filtered[:80]:
                lines.append(f"- `{item}`")
            if len(filtered) > 80:
                lines.append(f"- 还有 {len(filtered) - 80} 项未显示。")
        else:
            lines.append("- 当前范围未发现。")

    lines.extend(
        [
            "",
            "## 建议动作",
            "",
            "- `/wiki-sort`：优先处理 `markitdown-input/` 的新增导入材料。",
            "- `/wiki-sort all`：全库检查坏链、缺少用途段、孤立笔记和疑似项目目录。",
            "- 对敏感路径只做路径级索引，不自动提取正文。",
            "- 需要移动或重命名时，优先启动 Obsidian 后通过 Obsidian CLI 执行。",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def maybe_open_report(report_path: Path, vault: Path) -> None:
    status = obsidian_status()
    if not status.get("command") or not status.get("running"):
        return
    # This bundled CLI may support only a subset of commands. Opening by URI is stable.
    rel_path = rel(report_path, vault)
    uri = f"obsidian://open?path={str(report_path)}"
    try:
        subprocess.run([status["command"], uri], timeout=5, check=False)
    except Exception:
        _ = rel_path


def main() -> int:
    args = parse_args()
    vault = Path(args.vault)
    if not vault.exists():
        raise SystemExit(f"Vault not found: {vault}")

    map_out = Path(args.map_out) if args.map_out else vault / "00-索引" / "_system" / "llm-wiki-map.json"
    report_out = Path(args.report_out) if args.report_out else vault / "99-收件箱" / "每日整理候选.md"
    data, health = build_map(vault)
    map_out.parent.mkdir(parents=True, exist_ok=True)
    map_out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    scope = scope_for(vault, args.scope)
    write_report(report_out, data, health, scope)
    if args.open_report:
        maybe_open_report(report_out, vault)
    print(json.dumps({"map": str(map_out), "report": str(report_out), "counts": data["counts"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
