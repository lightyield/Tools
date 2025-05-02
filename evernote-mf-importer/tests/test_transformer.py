import sys
import os

# ✅ srcディレクトリをimportパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from transformer import transform_notes

def test_transform_notes_valid():
    titles = [
        "2025.01.01_接待交際費_スターバックス_1,100円_Aさん"
    ]
    records = transform_notes(titles)
    assert len(records) == 1
    record = records[0]
    assert record["取引日"] == "2025/01/01"
    assert record["借方勘定科目"] == "接待交際費"
    assert record["貸方勘定科目"] == "未払金"
    assert record["借方金額(円)"] == 1100
    assert record["摘要"] == "スターバックス"
    assert record["仕訳メモ"] == "Aさん"

def test_transform_notes_valid_without_memo():
    titles = [
        "2025.02.15_通信費_NTTドコモ_3,300円"
    ]
    records = transform_notes(titles)
    assert len(records) == 1
    record = records[0]
    assert record["取引日"] == "2025/02/15"
    assert record["借方勘定科目"] == "通信費"
    assert record["貸方勘定科目"] == "未払金"
    assert record["借方金額(円)"] == 3300
    assert record["摘要"] == "NTTドコモ"
    assert record["仕訳メモ"] == ""  # 空文字でOK

def test_transform_notes_invalid():
    titles = ["invalid_format_title"]
    records = transform_notes(titles)
    assert len(records) == 0  # スキップされる
