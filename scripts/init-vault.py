#!/usr/bin/env python3
"""Initialize a portable Obsidian LLM Wiki vault layout."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


DIRS: list[tuple[str, str]] = [
    ("00-索引", "全局入口、主题地图、检索索引和系统生成文件。"),
    ("00-索引/_system", "索引器生成的机器可读文件。"),
    ("01-概念", "稳定概念、机制、术语和原理。"),
    ("02-模型", "模型家族、具体模型、能力边界和版本记录。"),
    ("03-提供方", "API 厂商、本地运行时、部署平台、计费和接入说明。"),
    ("04-工具", "CLI、SDK、MCP server、向量数据库、评估库和 agent 框架。"),
    ("05-工作流", "可复用流程、检查清单、命令序列和故障排查。"),
    ("06-提示词", "prompt 模板、提示词模式、评估提示词和 agent 协作模板。"),
    ("07-评估", "benchmark、测试集、评估维度、结果记录和复盘。"),
    ("08-来源", "论文、官方文档、changelog、发布说明和文章资料卡。"),
    ("09-日记", "每日观察、实验过程、学习记录和临时想法。"),
    ("99-收件箱", "暂存材料、待归档摘录和尚未分类的内容。"),
    ("markitdown-input", "MarkItDown 转换后的 Markdown 输入区。"),
]


def note(title: str, purpose: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    return f"""---
类型: 索引
状态: 草稿
标签:
  - LLM/wiki
  - 索引
更新: {today}
---

# {title}

## 用途

{purpose}

## 入口

- [[00-索引/Home|Home]]
"""


def write_once(path: Path, content: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an Obsidian LLM Wiki vault.")
    parser.add_argument("--vault", required=True, help="Vault root path to create or update.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated starter notes.")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    created: list[str] = []
    for rel_path, purpose in DIRS:
        path = vault / rel_path
        path.mkdir(parents=True, exist_ok=True)
        created.append(str(path))
        if rel_path and not rel_path.endswith("_system"):
            title = Path(rel_path).name
            if rel_path != "markitdown-input":
                write_once(path / "说明.md", note(f"{title}说明", purpose), args.force)

    home = """---
类型: 索引
状态: 草稿
标签:
  - LLM/wiki
  - 索引
更新: {today}
---

# LLM Wiki Home

## 用途

这是本 Obsidian LLM Wiki 的总入口，用于连接概念、模型、工具、工作流、来源材料和每日整理报告。

## 目录

- [[00-索引/说明|索引]]
- [[01-概念/说明|概念]]
- [[02-模型/说明|模型]]
- [[03-提供方/说明|提供方]]
- [[04-工具/说明|工具]]
- [[05-工作流/说明|工作流]]
- [[06-提示词/说明|提示词]]
- [[07-评估/说明|评估]]
- [[08-来源/说明|来源]]
- [[09-日记/说明|日记]]
- [[99-收件箱/说明|收件箱]]
- [[99-收件箱/每日整理候选|每日整理候选]]
""".format(today=datetime.now().strftime("%Y-%m-%d"))
    write_once(vault / "00-索引" / "Home.md", home, args.force)
    write_once(vault / "99-收件箱" / "每日整理候选.md", note("每日整理候选", "由 `llm-wiki-indexer.py` 刷新的整理候选和健康检查报告。"), args.force)

    print(f"Vault initialized: {vault}")
    print(f"Directories touched: {len(created)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
