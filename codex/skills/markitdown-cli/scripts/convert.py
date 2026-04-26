#!/usr/bin/env python3
"""Small wrapper around the installed markitdown CLI."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


DEFAULT_VAULT = Path(os.environ.get("LLM_WIKI_VAULT", "~/Obsidian/LLM-Wiki")).expanduser()
DEFAULT_OUTPUT_ROOT = DEFAULT_VAULT / "markitdown-input"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert an input file or URL to Markdown with markitdown."
    )
    parser.add_argument("input", help="Input file path, URL, or '-' for stdin.")
    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Markdown output file or destination directory. Defaults to "
            f"{DEFAULT_OUTPUT_ROOT}/YYYYMMDD."
        ),
    )
    parser.add_argument(
        "--name",
        help="Output filename stem to use when --output is a directory or omitted.",
    )
    parser.add_argument("-x", "--extension", help="File extension hint, such as .pdf.")
    parser.add_argument("-m", "--mime-type", help="MIME type hint.")
    parser.add_argument("-c", "--charset", help="Charset hint, such as UTF-8.")
    parser.add_argument("-p", "--use-plugins", action="store_true", help="Enable plugins.")
    parser.add_argument("--keep-data-uris", action="store_true", help="Keep data URIs.")
    parser.add_argument("--force", action="store_true", help="Overwrite output if it exists.")
    return parser


def safe_stem(value: str) -> str:
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip(".-")
    return stem or "markitdown-output"


def derive_stem(input_value: str) -> str:
    if input_value == "-":
        return "markitdown-stdin"

    parsed = urlparse(input_value)
    if parsed.scheme and parsed.netloc:
        path_stem = Path(parsed.path).stem
        base = path_stem or parsed.netloc
        return safe_stem(base)

    path = Path(input_value).expanduser()
    return safe_stem(path.stem or path.name)


def resolve_output(output_arg: str | None, input_value: str, name: str | None) -> Path:
    stem = safe_stem(name) if name else derive_stem(input_value)
    filename = f"{stem}.md"

    if output_arg is None:
        date_folder = datetime.now().strftime("%Y%m%d")
        return DEFAULT_OUTPUT_ROOT / date_folder / filename

    output = Path(output_arg).expanduser()
    if output.suffix.lower() == ".md":
        return output

    return output / filename


def main() -> int:
    args = build_parser().parse_args()
    markitdown = shutil.which("markitdown")
    if markitdown is None:
        print("markitdown was not found on PATH", file=sys.stderr)
        return 127

    output = resolve_output(args.output, args.input, args.name)
    if output.exists() and not args.force:
        print(f"Refusing to overwrite existing output: {output}", file=sys.stderr)
        print("Pass --force to overwrite.", file=sys.stderr)
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = [markitdown]
    if args.input != "-":
        cmd.append(args.input)
    if args.extension:
        cmd.extend(["--extension", args.extension])
    if args.mime_type:
        cmd.extend(["--mime-type", args.mime_type])
    if args.charset:
        cmd.extend(["--charset", args.charset])
    if args.use_plugins:
        cmd.append("--use-plugins")
    if args.keep_data_uris:
        cmd.append("--keep-data-uris")
    cmd.extend(["--output", str(output)])

    result = subprocess.run(cmd)
    if result.returncode != 0:
        return result.returncode

    if not output.exists() or output.stat().st_size == 0:
        print(f"Conversion finished but output is missing or empty: {output}", file=sys.stderr)
        return 3

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
