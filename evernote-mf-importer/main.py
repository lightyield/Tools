import os
from datetime import datetime
from src.parser import parse_enex
from src.transformer import transform_notes
from src.exporter import export_to_csv

def main():
    downloads_dir = os.path.expanduser("~/Downloads")
    input_file = os.path.join(downloads_dir, "0.未整理.enex")

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(downloads_dir, f"MFimport_{timestamp}.csv")

    if not os.path.exists(input_file):
        print(f"入力ファイルが見つかりません: {input_file}")
        return

    print(f"読み込み中: {input_file}")
    notes = parse_enex(input_file)
    records = transform_notes(notes)
    export_to_csv(records, output_file)
    print(f"完了: {output_file} に出力しました。")

if __name__ == "__main__":
    main()
