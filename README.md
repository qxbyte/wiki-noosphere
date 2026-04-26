# Wiki Noosphere

`wiki-noosphere` 是一套面向 Obsidian 的本地 LLM Wiki 启动套件。它提供 Claude Code commands、Claude/Codex skills、MarkItDown 转换辅助脚本和 vault 索引器，用来快速创建、导入、整理和维护一套中文优先、适合检索和双链浏览的 Markdown 知识库。

项目的核心思路是：脚本和运行程序保留在本项目中，Obsidian vault 只保存知识库内容。用户安装本项目后，在 Claude Code 或 Codex 中输入 startup 指令，即可由 agent 初始化 vault 目录、生成首页和首份索引报告。

## 适合谁

- 想把 PDF、网页、Office 文档、模型文档、工具资料整理到 Obsidian 的用户。
- 想用 Claude Code 或 Codex 通过 skill/command 维护本地知识库的用户。
- 想把已有 LLM Wiki 工作流迁移到另一台 Mac、Windows PC 或 Linux 机器的用户。

## 项目包含什么

```text
wiki-noosphere/
├── claude/
│   ├── commands/
│   │   ├── llm-wiki-startup.md
│   │   ├── markitdown-cli.md
│   │   ├── llm-wiki-obsidian.md
│   │   └── wiki-sort.md
│   └── skills/
│       ├── harness-hub/
│       ├── llm-wiki-startup/
│       ├── llm-wiki-obsidian/
│       ├── markitdown-cli/
│       └── wiki-sort/
├── codex/
│   ├── commands/
│   │   ├── llm-wiki-startup.md
│   │   └── markitdown-cli.md
│   └── skills/
│       ├── harness-hub/
│       ├── llm-wiki-startup/
│       ├── llm-wiki-obsidian/
│       ├── markitdown-cli/
│       └── wiki-sort/
├── scripts/
│   ├── convert.py
│   ├── init-vault.py
│   ├── install.sh
│   └── llm-wiki-indexer.py
├── LICENSE
└── README.md
```

说明：

- `claude/commands`：Claude Code 斜杠命令，当前包含 `/llm-wiki-startup`、`/markitdown-cli`、`/llm-wiki-obsidian` 和 `/wiki-sort`。
- `claude/skills`：Claude Code 使用的 skills。
- `codex/commands`：Codex 命令入口。当前包含 `/llm-wiki-startup` 和 `/markitdown-cli`；是否自动读取取决于本机 Codex 版本，不能读取时用同名 skill 或自然语言触发。
- `codex/skills`：Codex 使用的 skills。
- `scripts/convert.py`：MarkItDown CLI 的封装，默认把转换结果写入 vault 的 `markitdown-input/YYYYMMDD/`。
- `scripts/init-vault.py`：首次初始化 Obsidian LLM Wiki vault 目录。
- `scripts/llm-wiki-indexer.py`：扫描 vault，生成检索地图和每日整理候选报告。
- `scripts/install.sh`：安装套件、复制 skills/commands。vault 初始化建议交给 Claude Code 或 Codex 端的 startup 指令完成。

本项目没有打包 Obsidian、Claude Code、Codex、Node.js、Python、MarkItDown 等外部程序。它只保存可迁移的工作流资产和必要脚本。

## 依赖软件

### 必装

1. Git

用于下载项目。

macOS:

```bash
xcode-select --install
```

Windows:

```powershell
winget install --id Git.Git -e
```

2. Python 3.12 或更新版本

`init-vault.py`、`convert.py`、`llm-wiki-indexer.py` 都使用 Python。Python 3.10+ 通常也能运行，但建议 3.12。

macOS:

```bash
brew install python@3.12
python3 --version
```

Windows:

```powershell
winget install --id Python.Python.3.12 -e
python --version
```

3. Node.js

Claude Code CLI 通常依赖 Node.js/npm 生态安装和运行。建议使用 LTS 版本。

macOS:

```bash
brew install node
node --version
npm --version
```

Windows:

```powershell
winget install OpenJS.NodeJS.LTS
node --version
npm --version
```

4. Obsidian

用于打开和浏览 Markdown vault。

macOS:

```bash
brew install --cask obsidian
```

Windows:

```powershell
winget install Obsidian.Obsidian
```

5. MarkItDown CLI

[MarkItDown](https://github.com/microsoft/markitdown) 是 Microsoft 开源的文档转换工具，可以把 PDF、Word、Excel、PowerPoint、HTML、图片、音频、压缩包、URL 等内容转换为 Markdown。本项目通过 `markitdown-cli` skill 和 `scripts/convert.py` 对它做了一层封装，默认把转换结果放进 Obsidian vault 的 `markitdown-input/YYYYMMDD/`。

推荐安装方式：

```bash
python3 -m pip install --user markitdown
markitdown --help
```

如果需要使用插件能力，可以按 MarkItDown 官方文档安装插件版本或运行：

```bash
markitdown --list-plugins
```

如果系统找不到 `markitdown`，需要把 Python user bin 加入 `PATH`。常见路径：

macOS/Linux:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Windows PowerShell:

```powershell
$env:Path += ";$env:APPDATA\Python\Python312\Scripts"
```

### 推荐安装

1. ripgrep

skills 会优先使用 `rg` 搜索本地 Markdown 和代码。

macOS:

```bash
brew install ripgrep
```

Windows:

```powershell
winget install BurntSushi.ripgrep.MSVC
```

2. Claude Code CLI

如果你主要使用 Claude Code，需要安装并登录 Claude Code CLI。安装方式可能随官方发布变化，请以 Anthropic/Claude Code 官方文档为准。安装后确认：

```bash
claude --help
```

3. Codex CLI 或 Codex 桌面端

如果你主要使用 Codex，需要安装对应客户端，并让 Codex 能读取 `~/.codex/skills`。

4. Obsidian CLI

Obsidian CLI 不是硬依赖。不同社区 CLI 语法不完全一致，本套 skills 会先检查 `obsidian --help` 或 `obsidian-cli --help`，可用时优先调用，不可用时直接编辑 Markdown 文件。

## 快速安装

1. 克隆项目

```bash
git clone https://github.com/YOUR_NAME/wiki-noosphere.git
cd wiki-noosphere
```

2. 一键安装到默认位置

```bash
bash scripts/install.sh
```

默认行为：

- 把项目复制到 `~/.wiki-noosphere`。
- 把 Claude commands 复制到 `~/.claude/commands`。
- 把 Claude skills 复制到 `~/.claude/skills`。
- 把 Codex commands 复制到 `~/.codex/commands`。
- 把 Codex skills 复制到 `~/.codex/skills`。
- 不立即初始化 Obsidian vault。初始化由 Claude Code 或 Codex 中的 startup 指令触发。

3. 推荐把环境变量写入 shell profile

macOS/Linux zsh:

```bash
cat >> ~/.zshrc <<'EOF'
export WIKI_NOOSPHERE_HOME="$HOME/.wiki-noosphere"
export LLM_WIKI_VAULT="$HOME/Obsidian/LLM-Wiki"
EOF
source ~/.zshrc
```

Windows PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("WIKI_NOOSPHERE_HOME", "$HOME\.wiki-noosphere", "User")
[Environment]::SetEnvironmentVariable("LLM_WIKI_VAULT", "$HOME\Obsidian\LLM-Wiki", "User")
```

4. 在 Claude Code 或 Codex 中开箱启动

Claude Code 推荐使用项目提供的 slash command：

```text
/llm-wiki-startup
```

指定 Obsidian vault 根目录：

```text
/llm-wiki-startup -path "~/Obsidian/LLM-Wiki"
```

你也可以在 Claude Code 或 Codex 对话里输入自然语言启动：

```text
start up llm-wiki
```

```text
start up llm-wiki -path "~/Obsidian/LLM-Wiki"
```

说明：很多 CLI 的 slash command 名称不支持空格，所以本项目提供的正式 Claude Code 命令是 `/llm-wiki-startup`。如果你输入 `/start up llm-wiki -path "..."`，agent 应把它当作自然语言启动请求处理，触发 `llm-wiki-startup` skill。

Codex 本机目录中可能存在 `~/.codex/commands`，本项目也会复制 `codex/commands/llm-wiki-startup.md`。如果你的 Codex 版本支持读取该目录，可以直接输入 `/llm-wiki-startup`；如果不支持，就输入 `start up llm-wiki -path "..."`，由 `llm-wiki-startup` skill 处理。

startup 会执行：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/init-vault.py" --vault "<vault-root>"
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "<vault-root>" --scope all
```

它会创建或确认目录结构，生成 `00-索引/Home.md`，刷新 `00-索引/_system/llm-wiki-map.json` 和 `99-收件箱/每日整理候选.md`。

5. 打开 Obsidian

在 Obsidian 中选择 `Open folder as vault`，打开：

```text
~/Obsidian/LLM-Wiki
```

## 自定义路径安装

如果你希望 vault 放在外置硬盘或同步盘：

```bash
bash scripts/install.sh \
  --kit-home "$HOME/.wiki-noosphere" \
  --vault "/path/to/your/Obsidian/LLM-Wiki"
```

安装时顺便初始化 vault，不通过 agent startup：

```bash
bash scripts/install.sh --init-vault
```

只安装 Claude Code 资产：

```bash
bash scripts/install.sh --claude-only
```

只安装 Codex 资产：

```bash
bash scripts/install.sh --codex-only
```

显式保持只安装 assets、不初始化 vault：

```bash
bash scripts/install.sh --no-init-vault
```

只测试项目复制，不写入 `~/.claude`、`~/.codex`，也不初始化 vault：

```bash
bash scripts/install.sh --kit-only --kit-home /tmp/wiki-noosphere-test
```

## 手动部署

如果不想使用安装脚本，可以手动复制。

Claude Code:

```bash
mkdir -p ~/.claude/commands ~/.claude/skills
cp -R claude/commands/* ~/.claude/commands/
cp -R claude/skills/* ~/.claude/skills/
```

Codex:

```bash
mkdir -p ~/.codex/commands ~/.codex/skills
cp -R codex/commands/* ~/.codex/commands/
cp -R codex/skills/* ~/.codex/skills/
```

脚本套件：

```bash
mkdir -p ~/.wiki-noosphere
cp -R scripts ~/.wiki-noosphere/
export WIKI_NOOSPHERE_HOME="$HOME/.wiki-noosphere"
export LLM_WIKI_VAULT="$HOME/Obsidian/LLM-Wiki"
```

脚本不要复制到 Obsidian vault 中。`scripts/` 应始终保留在项目安装目录，例如：

```text
macOS/Linux: ~/.wiki-noosphere/scripts/
Windows:     %USERPROFILE%\.wiki-noosphere\scripts\
```

skills 和 commands 通过 `WIKI_NOOSPHERE_HOME` 定位这些脚本，因此不依赖用户机器上的个人绝对路径。

初始化 vault：

```bash
python3 "$WIKI_NOOSPHERE_HOME/scripts/init-vault.py" --vault "$LLM_WIKI_VAULT"
```

## Vault 目录结构

执行 `/llm-wiki-startup` 后会创建或确认以下目录：

```text
00-索引/
00-索引/_system/
01-概念/
02-模型/
03-提供方/
04-工具/
05-工作流/
06-提示词/
07-评估/
08-来源/
09-日记/
99-收件箱/
markitdown-input/
```

同时会创建或刷新以下关键文件：

```text
00-索引/Home.md
00-索引/_system/llm-wiki-map.json
99-收件箱/每日整理候选.md
```

其中 `00-索引/Home.md` 和各主要目录的 `说明.md` 由初始化脚本创建；`00-索引/_system/llm-wiki-map.json` 和 `99-收件箱/每日整理候选.md` 会在 startup 运行首轮索引后生成或刷新。

## markitdown-input 是什么

`markitdown-input/` 是新导入材料的暂存区。推荐流程：

1. 用 MarkItDown 把 PDF、网页、docx、xlsx、pptx 等资料转换成 Markdown。
2. 输出到 `markitdown-input/YYYYMMDD/`。
3. 运行 `/wiki-sort` 扫描新输入。
4. 查看 `99-收件箱/每日整理候选.md`。
5. 再让 agent 按 LLM Wiki 规则归档、拆分、建立索引和双链。

示例：

```bash
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" ~/Downloads/paper.pdf
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" https://example.com/article --name example-article
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" ~/Downloads/report.docx --output "$LLM_WIKI_VAULT/markitdown-input/manual"
```

转换后运行：

```bash
python "$WIKI_NOOSPHERE_HOME/scripts/llm-wiki-indexer.py" --vault "$LLM_WIKI_VAULT" --scope markitdown-input
```

## Claude Code 使用

安装后，Claude Code 会读取：

```text
~/.claude/commands/
~/.claude/skills/
```

### /llm-wiki-obsidian

用途：让 Claude Code 按中文优先的 LLM Wiki 规则整理当前 Obsidian vault。

示例：

```text
/llm-wiki-obsidian 请为 04-工具 下的 Claude Code、Codex、MarkItDown 建立工具索引
```

```text
/llm-wiki-obsidian 把 markitdown-input/20260426 中的资料整理为来源笔记，并链接到 00-索引/Home
```

### /wiki-sort

用途：扫描 `markitdown-input/`，生成整理候选报告。默认只生成报告，不移动、不删除、不改写原始笔记。

示例：

```text
/wiki-sort
```

实际运行的命令等价于：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}" --scope markitdown-input
```

### /wiki-sort all

用途：扫描整个 vault，检查坏链、孤立笔记、重复标题、缺少用途段等。

示例：

```text
/wiki-sort all
```

实际运行的命令等价于：

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/llm-wiki-indexer.py" --vault "${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}" --scope all
```

### /llm-wiki-startup

用途：首次开箱启动 LLM Wiki。它会根据默认路径或 `-path` 指定路径创建 Obsidian vault 目录、生成说明页、建立 Home 入口，并运行首轮全库索引。

默认路径：

```text
${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}
```

示例：

```text
/llm-wiki-startup
```

```text
/llm-wiki-startup -path "~/Obsidian/LLM-Wiki"
```

自然语言等价写法：

```text
start up llm-wiki -path "~/Obsidian/LLM-Wiki"
```

## Codex 使用

Codex 使用 skills；部分 Codex 版本也会读取 `~/.codex/commands`。安装后，本项目会放置：

```text
~/.codex/commands/
~/.codex/skills/
```

如果你的 Codex 支持 commands，可以直接输入：

```text
/llm-wiki-startup
```

推荐在 Codex 中直接输入自然语言触发对应 skill：

```text
start up llm-wiki
```

```text
start up llm-wiki -path "~/Obsidian/LLM-Wiki"
```

```text
使用 llm-wiki-obsidian，把当前 vault 的 04-工具 建成工具索引
```

```text
/wiki-sort
```

```text
使用 markitdown-cli，把 ~/Downloads/report.pdf 转成 Markdown 并放入 markitdown-input
```

如果 Codex 没有自动继承环境变量，可以在任务中明确 vault：

```text
LLM_WIKI_VAULT 是 ~/Obsidian/LLM-Wiki，请运行 wiki-sort all 并总结报告。
```

## 基于知识库提问

安装并运行 `/llm-wiki-startup` 后，Claude Code 可以通过 `llm-wiki-obsidian` skill 按索引链路检索本地 Obsidian LLM Wiki。推荐在问题里明确写出“基于本地 LLM Wiki”或“基于我的 Obsidian 知识库”，这样 agent 会按 skill 中的“问答检索流程”工作：先读 `00-索引/Home.md`，再根据问题进入相关分类索引，只读取回答所需的链接笔记。

Claude Code 命令示例：

```text
/llm-wiki-obsidian 请基于本地 LLM Wiki 回答：Claude Code 和 Codex 在本项目中的部署差异是什么？
```

```text
/llm-wiki-obsidian 请基于我的 Obsidian LLM Wiki 检索：MarkItDown 导入资料后应该怎么整理？请说明依据来自哪些笔记。
```

自然语言示例：

```text
请使用 llm-wiki-obsidian，基于本地 LLM Wiki 回答：我应该如何维护 04-工具 目录？
```

```text
基于我的 Obsidian LLM Wiki 检索一下 RAG 评估相关笔记，只读取必要的索引和链接笔记，并在回答末尾列出依据笔记。
```

Codex 中也可以用同样的自然语言触发：

```text
使用 llm-wiki-obsidian，基于本地 LLM Wiki 回答：wiki-sort 和 markitdown-input 的关系是什么？
```

如果刚导入新资料，先运行 `/wiki-sort`；如果想让回答覆盖全库健康状态或旧资料关系，先运行 `/wiki-sort all` 刷新检索地图和整理候选报告。

## Claude Code 和 Codex 的部署差异

Claude Code:

- commands 放在 `~/.claude/commands`。
- skills 放在 `~/.claude/skills`。
- `/wiki-sort`、`/llm-wiki-obsidian` 这类 slash command 可直接触发。
- 更适合通过命令模板固定工作流入口。

Codex:

- commands 放在 `~/.codex/commands`。是否可用取决于当前 Codex 版本；不可用时不影响 skills。
- skills 放在 `~/.codex/skills`。
- 通过 command、skill 描述、自然语言、或明确输入 `/wiki-sort` 触发。
- 更适合在工程项目里结合代码搜索、脚本验证、README/交付文档一起处理。

共同点：

- 两者都使用同一套 portable scripts。
- 两者都可以维护同一个 Obsidian vault。
- 两者都应避免把私人 vault 内容发送到网络服务，除非用户明确允许。

## Skills 说明和示例

### llm-wiki-startup

用途：首次开箱启动 Obsidian LLM Wiki。安装项目资产后，用户在 Claude Code 或 Codex 端输入启动指令，由 agent 调用本项目脚本初始化目录和首轮索引。

支持的输入形式：

```text
/llm-wiki-startup
```

```text
/llm-wiki-startup -path "~/Obsidian/LLM-Wiki"
```

```text
start up llm-wiki -path "~/Obsidian/LLM-Wiki"
```

如果没有指定 `-path`，默认使用当前用户目录下的：

```text
~/Obsidian/LLM-Wiki
```

启动后会生成或刷新：

```text
00-索引/Home.md
00-索引/_system/llm-wiki-map.json
99-收件箱/每日整理候选.md
markitdown-input/
```

### llm-wiki-obsidian

用途：创建、整理、重构或维护本地 Obsidian LLM Wiki。

它会优先采用中文目录模型：

```text
00-索引/
01-概念/
02-模型/
03-提供方/
04-工具/
05-工作流/
06-提示词/
07-评估/
08-来源/
09-日记/
99-收件箱/
```

示例：

```text
请使用 llm-wiki-obsidian，为 MCP、RAG、工具调用分别创建概念笔记，并加入 01-概念/说明.md。
```

```text
请检查 02-模型 下面有没有重复标题，把重复项列出来，不要直接删除。
```

### wiki-sort

用途：运行索引器，生成 `llm-wiki-map.json` 和 `每日整理候选.md`。

示例：

```text
/wiki-sort
```

```text
/wiki-sort all
```

命令行手动运行：

```bash
python "$WIKI_NOOSPHERE_HOME/scripts/llm-wiki-indexer.py" --vault "$LLM_WIKI_VAULT" --scope markitdown-input
python "$WIKI_NOOSPHERE_HOME/scripts/llm-wiki-indexer.py" --vault "$LLM_WIKI_VAULT" --scope all
```

### markitdown-cli

用途：调用 Microsoft 开源的 [MarkItDown](https://github.com/microsoft/markitdown)，把外部资料转换为 Markdown，并把结果放到 `markitdown-input/YYYYMMDD/`，方便后续用 `/wiki-sort` 生成整理候选。

示例：

```text
/markitdown-cli ~/Downloads/openai-doc.pdf
```

```text
/markitdown-cli https://example.com/post --name example-post
```

```text
使用 markitdown-cli，把 ~/Downloads/openai-doc.pdf 转成 Markdown。
```

命令行等价用法：

```bash
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" ~/Downloads/openai-doc.pdf
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" ~/Downloads/slides.pptx --name openai-slides
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" https://example.com/post --name example-post
```

常用参数：

- `--output /path/to/file.md`：指定输出文件。
- `--output /path/to/directory`：指定输出目录。
- `--name custom-name`：为 URL、stdin 或复杂文件名指定输出文件名。
- `--extension .pdf`：在输入缺少扩展名时提示文件类型。
- `--use-plugins`：启用已安装的 MarkItDown 插件。

### harness-hub

用途：把需求按工程交付方式闭环，适合需要方案、实现、测试、复核和交付说明的开发任务。

示例：

```text
使用 Harness Hub，帮我给 llm-wiki-indexer 增加一个 --strict 模式，并补充 README。
```

注意：只有当任务确实较复杂，或用户明确要求 Harness Hub 多角色模式时，才需要启用多角色/子代理协作。简单单文件改动不必强行使用。

## 索引器行为

`llm-wiki-indexer.py` 会：

- 扫描 vault 中的 Markdown 文件。
- 解析 frontmatter、标题、wikilink、标签、别名、摘要。
- 生成 `00-索引/_system/llm-wiki-map.json`。
- 生成 `99-收件箱/每日整理候选.md`。
- 检查坏链、孤立笔记、缺少用途段、重复标题、疑似项目目录。
- 对敏感路径只做路径级索引，避免自动摘取正文摘要。

敏感路径规则默认包含：

```text
账号
激活
权限申请
系统
```

## 常见维护流程

### 导入一份 PDF

```bash
python "$WIKI_NOOSPHERE_HOME/scripts/convert.py" ~/Downloads/paper.pdf
python "$WIKI_NOOSPHERE_HOME/scripts/llm-wiki-indexer.py" --vault "$LLM_WIKI_VAULT" --scope markitdown-input
```

然后对 agent 说：

```text
请使用 llm-wiki-obsidian，阅读每日整理候选，把刚导入的 paper 拆成来源笔记和相关概念笔记。
```

### 做全库健康检查

```bash
python "$WIKI_NOOSPHERE_HOME/scripts/llm-wiki-indexer.py" --vault "$LLM_WIKI_VAULT" --scope all
```

然后打开：

```text
99-收件箱/每日整理候选.md
```

### 迁移到新电脑

1. 安装 Git、Python、Node.js、Obsidian、MarkItDown、Claude Code 或 Codex。
2. clone 本项目。
3. 运行 `bash scripts/install.sh --vault "你的 vault 路径"`。
4. 如果已有 vault，把旧 vault 内容复制到新 vault 路径。
5. 运行 `/wiki-sort all` 检查坏链和索引状态。

## Windows 注意事项

本项目的 `install.sh` 适合 macOS/Linux/Git Bash/WSL。Windows 用户有三种选择：

- 使用 WSL 运行安装脚本。
- 使用 Git Bash 运行安装脚本。
- 按“手动部署”章节复制文件。

PowerShell 下路径建议写成：

```powershell
$env:WIKI_NOOSPHERE_HOME="$HOME\.wiki-noosphere"
$env:LLM_WIKI_VAULT="$HOME\Obsidian\LLM-Wiki"
python "$env:WIKI_NOOSPHERE_HOME\scripts\init-vault.py" --vault "$env:LLM_WIKI_VAULT"
```

## 许可

默认使用 MIT License。若 skills 中包含第三方授权材料，请在发布前逐一确认 license。
