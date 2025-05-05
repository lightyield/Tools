#!/bin/bash
cd "$(dirname "$0")"   # スクリプトのあるディレクトリに移動
source .venv/bin/activate
python3 main.py
