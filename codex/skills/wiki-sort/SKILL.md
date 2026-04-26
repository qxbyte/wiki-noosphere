---
name: wiki-sort
description: Use when the user types /wiki-sort or /wiki-sort all to organize the local Obsidian LLM Wiki. /wiki-sort scans and prepares整理候选 for markitdown-input; /wiki-sort all scans the whole vault. Prefer Obsidian CLI for vault operations and use the local llm-wiki indexer.
---

# Wiki Sort

## Purpose

Handle `/wiki-sort` commands for the local Obsidian LLM Wiki at:

```text
${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}
```

This skill does not automatically move, delete, or rewrite source notes. It generates retrieval/index health artifacts and then uses `llm-wiki-obsidian` rules for any follow-up curation.

## Command Routing

- `/wiki-sort`: scan `markitdown-input/` and generate the daily整理候选 report.
- `/wiki-sort all`: scan the whole vault and generate the daily整理候选 report.

Run:

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}" --scope markitdown-input
```

or:

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}" --scope all
```

Outputs:

- `00-索引/_system/llm-wiki-map.json`
- `99-收件箱/每日整理候选.md`

## Workflow

1. Detect Obsidian CLI with `command -v obsidian` and whether Obsidian is running.
2. Run the indexer with the requested scope.
3. Read the generated report summary.
4. If the user asks to apply changes, use `llm-wiki-obsidian` and prefer Obsidian CLI for create/move/rename operations.
5. Do not extract sensitive content from `工作/权限申请/`, `工作/系统/`, `99-收件箱/账号/`, or `99-收件箱/激活/`; keep those path-level only unless the user explicitly asks for a specific local summary.

## Safety

- Default mode is dry-run/report generation.
- Do not delete files.
- Do not move or rename notes without explicit user confirmation.
- Do not transmit private vault content to network services.
