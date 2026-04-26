---
description: 使用本地 llm-wiki-obsidian skill，把 Obsidian vault 整理为中文优先的 LLM Wiki 知识库。
---

使用已安装的 `/llm-wiki-obsidian` skill。

请按照 `~/.claude/skills/llm-wiki-obsidian/SKILL.md 或本项目 claude/skills/llm-wiki-obsidian/SKILL.md` 的规范，整理、创建或维护当前 Obsidian vault。默认中文优先：目录说明、笔记用途、摘要、正文说明、标签和索引都尽量使用中文；LLM、API、MCP、CLI、SDK、RAG、OpenAI、Claude Code、Obsidian CLI 等专有名词可以保留英文。

每篇新笔记都要包含“用途”段落，说明它在知识库中的作用。新建目录时应包含中文说明页或索引页。若当前工作区不是明确的 Obsidian vault，请先定位活动 vault，必要时询问用户路径。
