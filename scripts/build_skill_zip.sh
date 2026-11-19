#!/usr/bin/env bash
# Rebuild docs/downloads/hack-kit-skill.zip from claude-ai/hack-kit/ (run after editing the claude.ai skill).
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
out="$root/docs/downloads/hack-kit-skill.zip"
mkdir -p "$(dirname "$out")"
rm -f "$out"
cd "$root/claude-ai" && zip -qr -X "$out" hack-kit
echo "Wrote $out"
