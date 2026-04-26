---
description: 扫描 Obsidian LLM Wiki 并生成整理候选报告
argument-hint: "[all]"
---

使用本地 `wiki-sort` skill 处理 Obsidian LLM Wiki 整理扫描。

## 命令语义

- `/wiki-sort`：只扫描 `markitdown-input/`，适合处理新导入文档。
- `/wiki-sort all`：扫描整个 Obsidian vault，适合做全库健康检查。

## 执行规则

如果 `$ARGUMENTS` 是 `all`，运行：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}" --scope all
```

否则运行：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}" --scope markitdown-input
```

然后用中文总结：

- 已生成或刷新 `00-索引/_system/llm-wiki-map.json`
- 已生成或刷新 `99-收件箱/每日整理候选.md`
- 命令输出中的统计信息

默认只生成报告，不移动、不删除、不改写原始笔记。除非用户明确要求并确认，否则不要执行文件移动、删除、重命名或正文改写。
