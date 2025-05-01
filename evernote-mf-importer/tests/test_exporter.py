import sys
import os
import csv
import tempfile

# ✅ srcディレクトリをimportパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from exporter import export_to_csv
from constants import CSV_HEADERS

def test_export_to_csv_creates_file():
    records = [
        {
            "取引日": "2025/01/01",
            "借方勘定科目": "接待交際費",
            "借方金額(円)": 1100,
            "貸方勘定科目": "未払金",
            "貸方金額(円)": 1100,
            "摘要": "スターバックス",
            "仕訳メモ": "Aさん"
        }
    ]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as f:
        export_to_csv(records, f.name)
        f.close()
        with open(f.name, newline='', encoding='shift_jis') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]["取引日"] == "2025/01/01"
            assert rows[0]["借方勘定科目"] == "接待交際費"
        os.unlink(f.name)
