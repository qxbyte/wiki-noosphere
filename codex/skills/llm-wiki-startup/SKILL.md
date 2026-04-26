---
name: llm-wiki-startup
description: 当用户想开箱启动、初始化、首次配置或 bootstrap 本地 Obsidian LLM Wiki 时使用。触发语包括 /llm-wiki-startup、start up llm-wiki、/start up llm-wiki、初始化 LLM Wiki、开箱启动 llm-wiki。
---

# LLM Wiki 开箱启动

## 目标

在用户安装本项目后，初始化一个本地 Obsidian LLM Wiki。该 skill 负责解析 vault 根目录、确认项目脚本存在、创建知识库目录结构、运行首轮索引，并告诉用户如何打开和继续使用 vault。

## 输入

- `-path` 或 `--path`：可选的 Obsidian vault 根目录。
- 如果没有提供路径，使用 `${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}`。
- 项目安装目录默认使用 `${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}`。

## 工作流

1. 解析 vault 路径：
   - 支持 `-path "..."`、`--path "..."`、`-path=...`、`--path=...`。
   - 展开 `~` 和环境变量。
   - 如果用户未指定路径，使用默认 vault 路径。
2. 确认项目脚本存在：
   - `scripts/init-vault.py`
   - `scripts/llm-wiki-indexer.py`
   - `scripts/convert.py`
3. 运行初始化和首轮索引：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/init-vault.py" --vault "<vault>"
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "<vault>" --scope all
```

4. 用中文汇报结果：
   - Vault 根目录。
   - 首页笔记：`00-索引/Home.md`。
   - 索引地图：`00-索引/_system/llm-wiki-map.json`。
   - 整理候选报告：`99-收件箱/每日整理候选.md`。
   - 导入目录：`markitdown-input/`。
5. 建议下一步命令：

```text
/wiki-sort
```

## 安全约束

- 不删除文件。
- 不移动或重命名已有笔记。
- 如果启动模板笔记已经存在，默认保留，除非用户明确要求覆盖。
- 不把私人 vault 内容发送到网络服务，除非用户明确授权。
