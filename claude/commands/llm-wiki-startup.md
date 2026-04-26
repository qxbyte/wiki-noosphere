---
description: 开箱启动 Obsidian LLM Wiki，初始化 vault 目录并生成首份索引报告。
argument-hint: "[-path <vault-root>]"
---

使用本地 `llm-wiki-startup` skill 开箱启动 LLM Wiki。

## 命令语义

- `/llm-wiki-startup`：在默认路径初始化 Obsidian vault。
- `/llm-wiki-startup -path "/path/to/vault"`：在指定根目录初始化 Obsidian vault。
- 用户也可能用自然语言输入：`start up llm-wiki -path "/path/to/vault"`。

## 执行规则

1. 从 `$ARGUMENTS` 中解析 `-path` 或 `--path` 后面的路径。
2. 如果没有提供路径，默认使用：

```bash
${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}
```

3. 确认本地 kit 路径：

```bash
${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}
```

4. 运行初始化脚本：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/init-vault.py" --vault "<解析后的 vault 路径>"
```

5. 运行首轮全库索引：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "<解析后的 vault 路径>" --scope all
```

6. 用中文总结：

- vault 根目录。
- 已创建或确认的目录。
- 已生成或刷新 `00-索引/_system/llm-wiki-map.json`。
- 已生成或刷新 `99-收件箱/每日整理候选.md`。
- 下一步建议：打开 Obsidian vault，导入资料到 `markitdown-input/`，然后运行 `/wiki-sort`。

默认不要删除、移动或改写用户已有笔记。若目标目录已有内容，只补齐缺失的目录和启动文件。

