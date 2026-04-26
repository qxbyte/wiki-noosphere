---
name: markitdown-cli
description: Convert local files, URLs, or stdin to Markdown using the installed MarkItDown CLI. Use when Codex needs to extract Markdown from PDFs, Office documents, spreadsheets, presentations, web pages, HTML, images with OCR, audio transcripts, archives, or other formats supported by `markitdown`, while preserving source files and producing clean `.md` outputs.
---

# MarkItDown CLI

## Overview

Use the local `markitdown` command to convert supported inputs into Markdown. Prefer this skill when the user asks to transform existing documents or media into `.md` for review, indexing, migration, wiki ingestion, or downstream editing.

## Workflow

1. Confirm the source path, URL, or stdin source. Do not modify or delete source files.
2. Locate MarkItDown with `command -v markitdown`; the expected local path must be available on `PATH`.
3. Choose an output path:
   - If the user gave an output file or destination directory, use it.
   - Otherwise, write to `${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}/markitdown-input/YYYYMMDD` using the source stem plus `.md`.
   - For URLs or stdin without a user-provided destination, write to the same dated Obsidian `markitdown-input/YYYYMMDD` directory with a descriptive `.md` filename.
4. Run MarkItDown through the bundled helper when a local output file is desired:

```bash
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/convert.py" INPUT
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/convert.py" INPUT --output /custom/directory
python "${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}/scripts/convert.py" INPUT --output /custom/file.md
```

5. Inspect the first part of the generated Markdown and file size. If the result is unexpectedly empty or noisy, retry with useful MarkItDown hints such as `--extension`, `--mime-type`, `--charset`, or `--use-plugins`.
6. Tell the user where the Markdown was written and mention any conversion warnings or limitations.

## Direct CLI Patterns

Use direct CLI calls when the task is simple or needs a MarkItDown option not exposed by the helper:

```bash
markitdown file.pdf -o file.md
markitdown file.docx --output file.md
markitdown input.bin --extension .xlsx -o output.md
markitdown --use-plugins input.any -o output.md
markitdown --list-plugins
```

For stdin:

```bash
markitdown --extension .html < page.html > page.md
```

## Options

- When no destination is specified, use `${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}/markitdown-input/YYYYMMDD` as the default output directory, where `YYYYMMDD` is the current date.
- Treat `--output /path/to/name.md` as an explicit file path.
- Treat `--output /path/to/directory` as a destination directory and generate `source-stem.md` inside it.
- Use `--name custom-name` with the helper when converting stdin, URLs, or files whose source name is not a good note title.
- Use `--extension` when reading from stdin or when a file lacks a reliable suffix.
- Use `--mime-type` or `--charset` when MarkItDown misidentifies content.
- Use `--use-plugins` only when installed plugins are needed; list them first with `--list-plugins`.
- Use `--use-docintel --endpoint ENDPOINT` only when the user explicitly wants Azure Document Intelligence and provides or confirms the endpoint.
- Avoid `--keep-data-uris` unless the user needs embedded base64 assets; it can create very large Markdown files.

## Quality Checks

- Check that the output file exists and is non-empty.
- Preview the top of the Markdown with `sed -n '1,80p' OUTPUT.md`.
- For large conversions, report size with `wc -c OUTPUT.md`.
- If the user needs layout fidelity, tables, or embedded images preserved exactly, explain that MarkItDown optimizes for Markdown extraction rather than pixel-perfect reconstruction.

## Bundled Helper

`scripts/convert.py` wraps the installed CLI for repeatable file conversion. It defaults to the Obsidian `markitdown-input/YYYYMMDD` directory when no output is specified, creates the destination directory if needed, refuses to overwrite an existing output unless `--force` is passed, and forwards selected MarkItDown hints.
