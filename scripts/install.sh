#!/usr/bin/env bash
set -euo pipefail

KIT_HOME="${WIKI_NOOSPHERE_HOME:-$HOME/.wiki-noosphere}"
VAULT="${LLM_WIKI_VAULT:-$HOME/Obsidian/LLM-Wiki}"
INSTALL_CLAUDE=1
INSTALL_CODEX=1
INIT_VAULT=0
INSTALL_USER_ASSETS=1

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [options]

Options:
  --kit-home PATH       Install portable kit files here. Default: ~/.wiki-noosphere
  --vault PATH          Obsidian vault path. Default: ~/Obsidian/LLM-Wiki
  --claude-only         Install Claude Code assets only
  --codex-only          Install Codex assets only
  --init-vault          Also initialize the Obsidian vault during install
  --kit-only            Copy this project to --kit-home only
  --no-init-vault       Keep install-only behavior. This is the default.
  -h, --help            Show help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --kit-home)
      KIT_HOME="$2"
      shift 2
      ;;
    --vault)
      VAULT="$2"
      shift 2
      ;;
    --claude-only)
      INSTALL_CODEX=0
      shift
      ;;
    --codex-only)
      INSTALL_CLAUDE=0
      shift
      ;;
    --init-vault)
      INIT_VAULT=1
      shift
      ;;
    --no-init-vault)
      INIT_VAULT=0
      shift
      ;;
    --kit-only)
      INSTALL_USER_ASSETS=0
      INSTALL_CLAUDE=0
      INSTALL_CODEX=0
      INIT_VAULT=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$KIT_HOME"
rsync -a --delete \
  --exclude '.git' \
  --exclude '.DS_Store' \
  "$ROOT/" "$KIT_HOME/"

if [[ "$INSTALL_USER_ASSETS" -eq 1 && "$INSTALL_CLAUDE" -eq 1 ]]; then
  mkdir -p "$HOME/.claude/commands" "$HOME/.claude/skills"
  rsync -a "$ROOT/claude/commands/" "$HOME/.claude/commands/"
  rsync -a "$ROOT/claude/skills/" "$HOME/.claude/skills/"
fi

if [[ "$INSTALL_USER_ASSETS" -eq 1 && "$INSTALL_CODEX" -eq 1 ]]; then
  mkdir -p "$HOME/.codex/skills"
  rsync -a "$ROOT/codex/skills/" "$HOME/.codex/skills/"
  if [[ -d "$ROOT/codex/commands" ]]; then
    mkdir -p "$HOME/.codex/commands"
    rsync -a "$ROOT/codex/commands/" "$HOME/.codex/commands/"
  fi
fi

if [[ "$INIT_VAULT" -eq 1 ]]; then
  python3 "$ROOT/scripts/init-vault.py" --vault "$VAULT"
fi

cat <<EOF
Installed wiki-noosphere.

Recommended shell profile exports:
export WIKI_NOOSPHERE_HOME="$KIT_HOME"
export LLM_WIKI_VAULT="$VAULT"
EOF

if [[ "$INSTALL_CLAUDE" -eq 1 ]]; then
  cat <<EOF
Claude assets:
  $HOME/.claude/commands
  $HOME/.claude/skills
EOF
fi

if [[ "$INSTALL_CODEX" -eq 1 ]]; then
  cat <<EOF
Codex assets:
  $HOME/.codex/commands
  $HOME/.codex/skills
EOF
fi

cat <<EOF
Vault:
  $VAULT
EOF
