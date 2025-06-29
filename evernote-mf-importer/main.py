import customtkinter as ctk
import tkinter.ttk as ttk
from tkinter import filedialog
from pathlib import Path
from datetime import datetime

from src.constants import CSV_HEADERS
from src.parser import parse_enex
from src.transformer import transform_notes
from src.exporter import export_to_csv

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.parsed_records = []
        self.source_file_path = None

        self.title("Evernote → MFクラウド会計 CSV変換ツール")
        self.geometry("1200x700")
        self.minsize(800, 600)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=0, column=0, pady=20)

        btn_browse = ctk.CTkButton(button_frame, text="ENEXファイル選択", command=self.select_file, width=200)
        btn_browse.pack(side="left", padx=10)

        label_arrow = ctk.CTkLabel(button_frame, text="-->")
        label_arrow.pack(side="left", padx=10)

        btn_convert = ctk.CTkButton(button_frame, text="MFクラウド会計向けCSV出力", command=self.convert, width=200)
        btn_convert.pack(side="left", padx=10)

        self.textbox = ctk.CTkTextbox(self, state="disabled", height=150)
        self.textbox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.tree = ttk.Treeview(self, columns=CSV_HEADERS, show="headings", height=10)
        for col in CSV_HEADERS:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=120)
        self.tree.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")

        scrollbar = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=0, sticky="ew", padx=20)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="ENEXファイルを選択",
            filetypes=[("ENEXファイル", "*.enex")]
        )
        if file_path:
            self.source_file_path = file_path

            self.textbox.configure(state="normal")
            self.textbox.delete("0.0", "end")

            for row in self.tree.get_children():
                self.tree.delete(row)

            try:
                try:
                    titles = parse_enex(file_path)
                except Exception as e:
                    self.textbox.insert("end", f"\n❌ エラー: ファイルのパースに失敗しました。\n{e}\n")
                    return

                try:
                    records, errors = transform_notes(titles)
                    self.parsed_records = records
                except Exception as e:
                    self.textbox.insert("end", f"\n❌ エラー: データの変換に失敗しました。\n{e}\n")
                    return

                self.textbox.insert("end", f"✅ 読み込み完了: {file_path}\n")

                if errors:
                    self.textbox.insert("end", "\n⚠️ 以下のノート題名はスキップされました：\n")
                    for i, (title, msg) in enumerate(errors, 1):
                        self.textbox.insert("end", f"{i:>2}. '{title}' → {msg}\n")

                self.textbox.insert("end", f"\n✅ 正常処理数：{len(records)} 件\n")
                self.textbox.insert("end", f"❌ スキップ数：{len(errors)} 件\n")

                for i, record in enumerate(records, start=1):
                    record["取引No"] = i
                    row = [record.get(h, "") for h in CSV_HEADERS]
                    self.tree.insert("", "end", values=row)

            finally:
                self.textbox.configure(state="disabled")

    def convert(self):
        self.textbox.configure(state="normal")

        if not self.parsed_records or not self.source_file_path:
            self.textbox.insert("end", "⚠️ 出力対象のデータがありません。\n")
            self.textbox.configure(state="disabled")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_path = Path(self.source_file_path).with_name(f"mf_journal_{timestamp}.csv")
            export_to_csv(self.parsed_records, str(output_path))
            self.textbox.insert("end", f"\n✅ 出力完了: {output_path}\n")
        except Exception as e:
            self.textbox.insert("end", f"\n❌ 出力エラー:\n{str(e)}\n")
        finally:
            self.textbox.configure(state="disabled")

if __name__ == '__main__':
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()