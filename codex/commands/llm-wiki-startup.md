# /llm-wiki-startup

开箱启动本地 Obsidian LLM Wiki，初始化 vault 目录并生成首份索引报告。

## 用法

```text
/llm-wiki-startup
/llm-wiki-startup -path "/path/to/vault"
start up llm-wiki -path "/path/to/vault"
```

## 规则

1. 读取 `~/.codex/skills/llm-wiki-startup/SKILL.md`。
2. 从参数中解析 `-path` 或 `--path`。
3. 如果没有指定路径，使用 `${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}`。
4. 使用 `${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}` 定位项目脚本。
5. 运行：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/init-vault.py" --vault "<vault>"
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "<vault>" --scope all
```

## 交付

用中文总结 vault 根目录、已生成的首页、索引地图、整理候选报告和下一步建议。不要删除、移动或重命名用户已有笔记。

