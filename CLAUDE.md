# CLAUDE.md

本文件是 Wiki Noosphere 项目中 Claude Code 的协作规则。

## 项目定位

- 本项目是 Obsidian LLM Wiki 的本地启动套件。
- 脚本和运行程序保留在项目安装目录中，不写入 Obsidian vault。
- Obsidian vault 只保存知识库内容、索引、整理候选和导入材料。

## 路径约定

- 使用 `WIKI_NOOSPHERE_HOME` 定位项目脚本，默认值为 `~/.wiki-noosphere`。
- 使用 `LLM_WIKI_VAULT` 定位 Obsidian vault，默认值为 `~/Obsidian/LLM-Wiki`。
- 不要在 commands、skills 或脚本中写入个人机器绝对路径。

## 写作与文档

- 面向用户的 README 内容应保持开源项目视角，避免出现个人本机路径、内部发布检查、私有仓库操作记录或会话历史。
- 中文说明优先；产品名、命令、API、CLI、SDK、LLM、RAG、MCP、MarkItDown 等专有名词可以保留英文。

## 提交规则

- Git 提交信息必须使用中文。
- 提交标题建议使用 `类型(范围): 主题` 格式，但类型、范围和主题都应使用中文，例如：`文档(说明): 补充知识库提问示例`。
- 提交正文使用中文说明具体修改点。
