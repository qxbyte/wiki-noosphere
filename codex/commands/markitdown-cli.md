# /markitdown-cli

使用 MarkItDown CLI 将文件、URL 或标准输入转换为 Markdown，并默认写入 Obsidian vault 的 `markitdown-input/YYYYMMDD/`。

## 用法

```text
/markitdown-cli ~/Downloads/file.pdf
/markitdown-cli https://example.com/article --name article
/markitdown-cli ~/Downloads/report.docx --output "$LLM_WIKI_VAULT/markitdown-input/manual"
```

## 规则

1. 读取 `~/.codex/skills/markitdown-cli/SKILL.md`。
2. 确认 `markitdown` 命令可用。
3. 默认运行：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/convert.py" <input>
```

4. 转换完成后，用中文总结输出路径，并提示可以运行 `/wiki-sort` 生成整理候选报告。

默认不删除、不移动源文件。

