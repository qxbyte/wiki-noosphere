---
name: llm-wiki-obsidian
description: Use this skill when asked to build, update, reorganize, or maintain a local LLM Wiki knowledge base with Claude Code and Obsidian CLI. Use for Obsidian vaults, Markdown wiki notes, model/provider/tool documentation, retrieval-oriented knowledge bases, and Karpas-style LLM Wiki curation workflows.
---

# LLM Wiki Obsidian

## Overview

Build and maintain a local Markdown knowledge base for LLM tooling and research, using Claude Code for reasoning/editing and Obsidian CLI for vault operations when available. Prefer source-backed, link-rich notes that stay useful in Obsidian and are friendly to search, backlinks, and future agent retrieval.

## First Moves

1. Locate the vault or repo root. Prefer an explicit user path; otherwise inspect the current workspace for `.obsidian/`, `README.md`, `index.md`, `Home.md`, or existing wiki folders.
2. Check available tools before assuming commands: `command -v obsidian`, `command -v obsidian-cli`, `command -v claude`, `command -v rg`.
3. Inspect existing conventions: folder names, frontmatter, tag style, note naming, index pages, templates, and link format.
4. If the user asks for current facts about models, libraries, companies, product behavior, pricing, releases, or docs, verify against primary or official sources before writing.
5. Preserve local user edits. Read relevant files before changing them and keep edits scoped to the requested knowledge area.

## Obsidian CLI Use

There are several community CLIs named for Obsidian. Do not assume one fixed syntax. Run `obsidian --help` or `obsidian-cli --help` and adapt to the installed command.

Use the CLI for operations it supports cleanly:

- Opening or validating a vault path.
- Creating, moving, renaming, or listing notes.
- Applying templates if the local CLI exposes that feature.
- Triggering Obsidian URI actions when the CLI is a wrapper around the desktop app.

Use direct Markdown edits when the CLI is missing, ambiguous, or less reliable than file operations. Keep resulting files valid Obsidian notes either way.

## Knowledge Model

Default to a Karpas-style LLM Wiki layout unless the vault already has a stronger convention:

```text
00-Index/
01-Concepts/
02-Models/
03-Providers/
04-Tools/
05-Workflows/
06-Prompts/
07-Evaluations/
08-Sources/
99-Inbox/
```

Core note types:

- **Index notes**: navigation, maps of content, topic entry points, and backlinks.
- **Concept notes**: durable ideas such as RAG, tool calling, context windows, evals, agents, MCP, embeddings, fine-tuning.
- **Entity notes**: models, providers, libraries, CLIs, APIs, datasets, papers, and products.
- **Workflow notes**: repeatable procedures, decision trees, commands, checklists, and failure modes.
- **Source notes**: compact records of important papers, docs, changelogs, posts, or release notes.

Prefer one durable idea per note. Use broader index notes to connect them instead of creating giant catch-all pages.

## Note Format

Follow existing vault style first. If no style exists, use this compact structure:

```markdown
---
type: concept
status: draft
tags:
  - llm/wiki
aliases: []
updated: YYYY-MM-DD
---

# Note Title

## Summary

Two to four sentences with the durable point.

## Details

- Key fact or explanation.
- Practical implication.
- Caveat or failure mode.

## Links

- Related: [[Another Note]]
- Source: [Official docs](https://example.com)
```

Rules:

- Use Obsidian wikilinks for internal references: `[[Note Title]]` or `[[Folder/Note Title|label]]`.
- Use normal Markdown links for external sources.
- Put volatile claims behind dates and sources.
- Use concise tags. Avoid tag explosions.
- Keep headings stable so backlinks and references do not break.
- When creating filenames, prefer readable title case Markdown files unless the vault already uses another style.

## Curation Workflow

For new topics:

1. Gather local context with `rg` and file reads.
2. Create or update the relevant index note first so the topic has a home.
3. Add atomic concept/entity/workflow/source notes as needed.
4. Link new notes bidirectionally where useful.
5. Add source URLs and retrieval-friendly summaries.
6. Run a quick validation pass: broken links, duplicate titles, inconsistent frontmatter, and missing index links.

For existing topics:

1. Read the note and its neighbors before editing.
2. Merge duplicates only when titles clearly refer to the same concept.
3. Preserve useful backlinks and aliases during moves/renames.
4. Add a short "Updated" or dated section only if chronology matters; otherwise integrate edits naturally.

## Retrieval Workflow

When the user asks a question based on the local Obsidian vault, do not start with a broad full-vault read. Route through indexes first:

1. Read `00-索引/Home.md`.
2. Choose the most relevant category index:
   - work, requirements, permissions, systems, projects: `00-索引/10-工作目录.md`
   - Java, Spring, Redis, architecture, middleware: `00-索引/01-概念.md`
   - Claude, Codex, Obsidian, MarkItDown: `00-索引/04-工具.md`
   - workflow, automation, delivery, wiki sorting: `00-索引/05-工作流.md`
   - imported or external material: `00-索引/08-来源.md`
3. If an index points to a project index, read the project index before source notes.
4. Read only the linked source notes needed to answer.
5. Mention the key notes used as evidence in the answer.

## Retrieval Index Requirements

Indexes should be more than navigation lists. When updating an index, include:

- A short topic summary.
- Keywords and aliases users may ask with.
- "Can answer" questions when useful.
- Entry links to project or topic indexes.
- Links to source notes.
- Sensitive-path handling notes when needed.

For sensitive work material such as `工作/权限申请/`, `工作/系统/`, `99-收件箱/账号/`, and `99-收件箱/激活/`, prefer path-level indexing and avoid extracting private details unless the user explicitly asks for a specific local summary.

## Local Indexer and Sorting

Use the local indexer for health checks and machine-readable retrieval maps:

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

When the user types `/wiki-sort`, use the `wiki-sort` skill and scan `markitdown-input/`. When the user types `/wiki-sort all`, scan the whole vault. These commands are dry-run/reporting by default.

## Obsidian CLI

Prefer Obsidian CLI for vault operations when available, especially creating, moving, renaming, opening, or validating notes. This local machine has `/usr/local/bin/obsidian`, which points to Obsidian.app's bundled `obsidian-cli`; some operations require the Obsidian desktop app to be running. If CLI is unavailable, fall back to direct Markdown reads and only perform file edits after respecting the user's request and safety constraints.

## Claude Code Collaboration

When coordinating with local Claude Code:

- Treat Claude Code as an optional local collaborator, not a required dependency.
- If the `claude` command exists, inspect `claude --help` before invoking it.
- Use Claude Code for bounded drafting, critique, or refactoring prompts; keep final writes under Codex control unless the user asks otherwise.
- Do not send private vault content to any networked service unless the user explicitly allows it.
- Record useful reusable prompts in `06-Prompts/` when the user asks for prompt assets or repeatable agent workflows.

## Validation

Before finishing:

- Run `rg -n "\\[\\[[^\\]]*$" <vault>` or an equivalent check for malformed wikilinks when practical.
- Search for duplicate note titles when creating many files.
- Confirm generated notes are linked from at least one index or neighboring note.
- If commands could not be run, say what was skipped and why.

For deeper style guidance, read `references/wiki-patterns.md`.
