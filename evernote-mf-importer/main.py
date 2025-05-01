import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from src.parser import parse_enex
from src.transformer import transform_notes
from src.exporter import export_to_csv

def select_enex_file():
    root = tk.Tk()
    root.withdraw()  # メインウィンドウは非表示にする
    file_path = filedialog.askopenfilename(
        title="Evernote ENEXファイルを選択",
        filetypes=[("Evernote Export Files", "*.enex")]
    )
    if file_path and file_path.endswith(".enex"):
        return file_path
    else:
        print("有効な .enex ファイルが選択されませんでした。")
        return None

def main():
    input_file = select_enex_file()
    if not input_file:
        return

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(os.path.dirname(input_file), f"mf_journal_{timestamp}.csv")

    print(f"読み込み中: {input_file}")
    notes = parse_enex(input_file)
    records = transform_notes(notes)
    export_to_csv(records, output_file)
    print(f"完了: {output_file} に出力しました。")

if __name__ == "__main__":
    main()
