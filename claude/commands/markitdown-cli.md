---
description: 使用 MarkItDown CLI 将文件、URL 或标准输入转换为 Markdown，并默认写入 markitdown-input。
argument-hint: "<input> [--output <path>] [--name <name>] [--extension .pdf]"
---

使用本地 `markitdown-cli` skill 处理文档转换。

## 命令语义

- `/markitdown-cli ~/Downloads/file.pdf`
- `/markitdown-cli https://example.com/article --name article`
- `/markitdown-cli ~/Downloads/report.docx --output "$LLM_WIKI_VAULT/markitdown-input/manual"`

## 执行规则

1. 读取 `markitdown-cli` skill。
2. 确认 `markitdown` 命令可用：

```bash
command -v markitdown
```

3. 默认使用项目脚本：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/convert.py" <input>
```

4. 如果用户提供 `--output`、`--name`、`--extension`、`--mime-type`、`--charset`、`--use-plugins` 等参数，按需转发给 `convert.py`。
5. 转换完成后，用中文总结输出文件路径、文件大小和是否需要运行 `/wiki-sort`。

默认不删除、不移动源文件。

