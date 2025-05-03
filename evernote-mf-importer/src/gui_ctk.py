import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog
from pathlib import Path
from datetime import datetime

from src.constants import CSV_HEADERS
from src.parser import parse_enex
from src.transformer import transform_notes
from src.exporter import export_to_csv

parsed_records = []
source_file_path = None  # 選択されたファイルパスを保持

def select_file():
    global parsed_records, source_file_path
    file_path = filedialog.askopenfilename(
        title="ENEXファイルを選択",
        filetypes=[("ENEXファイル", "*.enex")]
    )
    if file_path:
        source_file_path = file_path  # CSV出力時に再利用

        textbox.configure(state="normal")
        textbox.delete("0.0", "end")

        for row in tree.get_children():
            tree.delete(row)

        try:
            titles = parse_enex(file_path)
            records, errors = transform_notes(titles)
            parsed_records = records

            textbox.insert("end", f"✅ 読み込み完了: {file_path}\n")

            if errors:
                textbox.insert("end", "\n⚠️ 以下のノート題名はスキップされました：\n")
                for i, (title, msg) in enumerate(errors, 1):
                    textbox.insert("end", f"{i:>2}. '{title}' → {msg}\n")

            textbox.insert("end", f"\n✅ 正常処理数：{len(records)} 件\n")
            textbox.insert("end", f"❌ スキップ数：{len(errors)} 件\n")

            for i, record in enumerate(records, start=1):
                record["取引No"] = i
                row = [record.get(h, "") for h in CSV_HEADERS]
                tree.insert("", "end", values=row)

        except Exception as e:
            textbox.insert("end", f"\n❌ エラーが発生しました:\n{str(e)}\n")
        finally:
            textbox.configure(state="disabled")

def convert():
    textbox.configure(state="normal")

    if not parsed_records or not source_file_path:
        textbox.insert("end", "⚠️ 出力対象のデータがありません。\n")
        textbox.configure(state="disabled")
        return

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = Path(source_file_path).with_name(f"mf_journal_{timestamp}.csv")
        export_to_csv(parsed_records, str(output_path))
        textbox.insert("end", f"\n✅ 出力完了: {output_path}\n")
    except Exception as e:
        textbox.insert("end", f"\n❌ 出力エラー:\n{str(e)}\n")
    finally:
        textbox.configure(state="disabled")

# UIセットアップ
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Evernote → MFクラウド会計 CSV変換ツール")
app.geometry("1200x700")
app.minsize(800, 600)

# グリッド構成
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=0)
app.grid_rowconfigure(2, weight=1)

# --- 中央配置用フレームを作成 ---
button_frame = ctk.CTkFrame(app, fg_color="transparent")
button_frame.grid(row=0, column=0, pady=20)

# フレーム内にボタンを横並びに配置
btn_browse = ctk.CTkButton(button_frame, text="ENEXファイル選択", command=select_file, width=200)
btn_browse.pack(side="left", padx=10)

label_arrow = ctk.CTkLabel(button_frame, text="-->")
label_arrow.pack(side="left", padx=10)

btn_convert = ctk.CTkButton(button_frame, text="MFクラウド会計向けCSV出力", command=convert, width=200)
btn_convert.pack(side="left", padx=10)

# --- コンソール ---
textbox = ctk.CTkTextbox(app, state="disabled", height=150)
textbox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# --- リスト表示 ---
tree = ttk.Treeview(app, columns=CSV_HEADERS, show="headings", height=10)
for col in CSV_HEADERS:
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=120)
tree.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")

# --- スクロールバー ---
scrollbar = ttk.Scrollbar(app, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=scrollbar.set)
scrollbar.grid(row=3, column=0, sticky="ew", padx=20)

app.mainloop()
