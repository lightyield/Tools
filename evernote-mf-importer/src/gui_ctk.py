import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from datetime import datetime
from src.parser import parse_enex
from src.transformer import transform_notes
from src.exporter import export_to_csv

def select_file():
    file_path = filedialog.askopenfilename(
        title="ENEXファイルを選択",
        filetypes=[("ENEXファイル", "*.enex")]
    )
    if file_path:
        entry_input.delete(0, ctk.END)
        entry_input.insert(0, file_path)

def convert():
    path = entry_input.get()
    textbox.configure(state="normal")
    textbox.delete("0.0", "end")

    if not path or not Path(path).exists():
        textbox.insert("end", "⚠️ 有効なENEXファイルを選択してください。\n")
        textbox.configure(state="disabled")
        return

    try:
        textbox.insert("end", f"読み込み中: {path}\n")
        titles = parse_enex(path)
        records, errors = transform_notes(titles)

        if errors:
            textbox.insert("end", "\n⚠️ 以下のノート題名はスキップされました：\n")
            for i, (title, msg) in enumerate(errors, 1):
                textbox.insert("end", f"{i:>2}. '{title}' → {msg}\n")

        # ✅ 件数情報を表示（ここが追加）
        textbox.insert("end", f"\n✅ 正常処理数：{len(records)} 件\n")
        textbox.insert("end", f"❌ スキップ数：{len(errors)} 件\n")

        if records:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = Path(path).with_name(f"mf_journal_{timestamp}.csv")
            export_to_csv(records, str(output_path))
            textbox.insert("end", f"\n✅ 出力完了: {output_path}\n")
        else:
            textbox.insert("end", "\n⚠️ 有効なレコードが見つかりませんでした。\n")

    except Exception as e:
        textbox.insert("end", f"\n❌ エラーが発生しました:\n{str(e)}\n")
    finally:
        textbox.configure(state="disabled")

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Evernote → MFクラウド CSV変換ツール")
app.geometry("800x500")
app.minsize(600, 400)

# グリッド設定
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(5, weight=1)

entry_input = ctk.CTkEntry(app)
entry_input.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

# ボタン幅は固定（旧スタイルと同様に）
btn_browse = ctk.CTkButton(app, text="ENEXファイル選択", command=select_file, width=200)
btn_browse.grid(row=1, column=0, pady=5)

btn_convert = ctk.CTkButton(app, text="CSV出力", command=convert, width=200)
btn_convert.grid(row=2, column=0, pady=10)

textbox = ctk.CTkTextbox(app, state="disabled")
textbox.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")

app.mainloop()
