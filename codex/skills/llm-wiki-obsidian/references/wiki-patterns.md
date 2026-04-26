# LLM Wiki Patterns

## Folder Responsibilities

- `00-Index/`: entry points, maps of content, topic dashboards.
- `01-Concepts/`: stable ideas and mechanisms.
- `02-Models/`: model families, individual models, context windows, modalities, known constraints.
- `03-Providers/`: API vendors, local runtimes, hosting platforms, billing or deployment notes.
- `04-Tools/`: CLIs, SDKs, MCP servers, vector databases, evaluation libraries, agent frameworks.
- `05-Workflows/`: repeatable operating procedures.
- `06-Prompts/`: reusable prompts, prompt patterns, evaluation prompts.
- `07-Evaluations/`: benchmark notes, harnesses, rubrics, test results.
- `08-Sources/`: source summaries for papers, docs, changelogs, release posts.
- `99-Inbox/`: temporary notes that should be triaged later.

## Naming

Prefer names people will search for:

- `Tool Calling.md`
- `OpenAI Responses API.md`
- `Claude Code.md`
- `Obsidian CLI.md`
- `RAG Evaluation.md`

Use aliases for alternate names, acronyms, or old names.

## Entity Note Template

```markdown
---
type: entity
status: draft
tags:
  - llm/wiki
aliases: []
updated: YYYY-MM-DD
---

# Entity Name

## Summary

What it is, why it matters, and when to use it.

## Capabilities

- Capability.
- Limitation.
- Integration point.

## Operational Notes

- Setup, commands, config, or compatibility notes.

## Links

- Related: [[Related Note]]
- Source: [Official docs](https://example.com)
```

## Source Note Template

```markdown
---
type: source
status: reference
tags:
  - llm/source
source_kind: docs
published:
updated: YYYY-MM-DD
---

# Source Title

## Citation

- URL:
- Author/Org:
- Accessed: YYYY-MM-DD

## Takeaways

- Stable takeaway.
- Versioned or date-sensitive takeaway.

## Connects To

- [[Concept]]
- [[Tool]]
```

## Link Hygiene

- Add new notes to the nearest index immediately.
- Prefer direct links in both directions when two notes are conceptually important to each other.
- Use aliases instead of duplicate pages for acronyms or renamed products.
- Keep one canonical page per concept or entity.

## Retrieval-Friendly Writing

- Put the answer-like summary near the top.
- Use exact product, API, model, and command names.
- Keep examples short and executable.
- Record dates for fast-moving facts.
- Separate stable concepts from release-specific details.
