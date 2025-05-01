#!/bin/bash
cd "$(dirname "$0")"
echo "📦 テストを開始します..."
PYTHONPATH="$(pwd)" pytest -v
