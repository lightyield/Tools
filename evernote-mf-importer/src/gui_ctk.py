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
    if not path or not Path(path).exists():
        textbox.configure(state="normal")
        textbox.delete("0.0", "end")
        textbox.insert("end", "⚠️ 有効なENEXファイルを選択してください。\n")
        textbox.configure(state="disabled")
        return

    try:
        textbox.configure(state="normal")
        textbox.insert("end", f"読み込み中: {path}\n")
        titles = parse_enex(path)
        records = transform_notes(titles)

        if records:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = Path(path).with_name(f"mf_journal_{timestamp}.csv")
            export_to_csv(records, str(output_path))
            textbox.insert("end", f"✅ 出力完了: {output_path}\n")
        textbox.configure(state="disabled")
    except Exception as e:
        textbox.insert("end", f"❌ エラー: {e}\n")
        textbox.configure(state="disabled")

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Evernote → MFクラウド CSV変換ツール")
app.geometry("600x350")

entry_input = ctk.CTkEntry(app, width=400)
entry_input.pack(pady=10)

btn_browse = ctk.CTkButton(app, text="ENEXファイル選択", command=select_file)
btn_browse.pack(pady=5)

btn_convert = ctk.CTkButton(app, text="CSV出力", command=convert)
btn_convert.pack(pady=10)

textbox = ctk.CTkTextbox(app, width=550, height=150, state="disabled")
textbox.pack(pady=10)

app.mainloop()
