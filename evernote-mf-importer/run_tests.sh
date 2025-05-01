#!/bin/bash
cd "$(dirname "$0")"
echo "📦 テストを開始します..."

# 仮想環境の pytest を明示的に指定
PYTHONPATH="$(pwd)" .venv/bin/pytest -v
