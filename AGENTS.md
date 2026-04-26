# AGENTS.md

本文件是 Wiki Noosphere 项目中 Codex/Agent 的协作规则。

## 项目定位

- 本项目是 Obsidian LLM Wiki 的本地启动套件。
- 脚本和运行程序保留在项目安装目录中，不写入 Obsidian vault。
- Obsidian vault 只保存知识库内容、索引、整理候选和导入材料。

## 路径约定

- 使用 `WIKI_NOOSPHERE_HOME` 定位项目脚本，默认值为 `~/.wiki-noosphere`。
- 使用 `LLM_WIKI_VAULT` 定位 Obsidian vault，默认值为 `~/Obsidian/LLM-Wiki`。
- 不要在 commands、skills 或脚本中写入个人机器绝对路径。

## 工作方式

- 修改前先读相关 commands、skills、README 和 scripts，保持现有结构。
- 不要把私有 Obsidian vault 内容、账号、激活码、API key、会话历史或本地缓存提交到仓库。
- 若需要验证 startup，使用临时目录或用户明确指定的 vault 路径。

## 提交规则

- Git 提交信息必须使用中文。
- 提交标题建议使用 `类型(范围): 主题` 格式，但类型、范围和主题都应使用中文，例如：`文档(说明): 补充知识库提问示例`。
- 提交正文使用中文说明具体修改点。
