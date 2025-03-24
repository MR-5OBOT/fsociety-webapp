import os
import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


class Tj_analyser:
    def __init__(self, root):
        self.root = root
        self.root.title("Tj_Analyser")
        self.root.geometry("300x250")
        self.root.resizable(True, True)

        self.style = ttk.Style(self.root)
        self.root.tk.call("source", "./Forest-ttk-theme/forest-dark.tcl")  # Load custom theme
        self.style.theme_use("forest-dark")  # Set custom theme
        self.style.configure("TButton", font=("Helvetica", 12), padding=5)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

        self.checkdir()
        self.widgets()

    def checkdir(self, directory="./exported_data"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[])
        if not file_path:
            return None
        df = pd.read_csv(file_path) if file_path.endswith(".csv") else pd.read_excel(file_path)
        required_cols = ["date", "outcome", "pl_by_percentage", "risk_by_percentage", "entry_time", "pl_by_rr"]
        if not all(col in df.columns for col in required_cols):
            messagebox.showerror("Error", f"Missing required columns: {', '.join(required_cols)}")
            return None

    def open_link(self):
        webbrowser.open("https://docs.google.com/spreadsheets/d/1JwaEanv8tku6dXSGWsu3c7KFZvCtEjQEcKkzO0YcrPQ/edit?usp=sharing")

    def update_status(self, message, color="green"):
        self.status_label.config(text=message, foreground=color)

    def on_upload(self):
        self.update_status("Uploading file...", "violet")
        df_storage = self.upload_file()
        if df_storage is not None:
            # self.process_data(df_storage)
            self.update_status("Data processed successfully", "violet")
        else:
            self.update_status("Upload failed", "red")

    def widgets(self):
        self.title_label = ttk.Label(self.root, text="Trading Journal Analyser", style="TLabel", font=("Helvetica", 16))
        self.title_label.grid(column=0, row=0, columnspan=2, pady=10, padx=10, sticky="n")

        self.cfds_tpl = ttk.Button(self.root, text="Journal Template", command=self.open_link)
        self.cfds_tpl.grid(column=0, row=1, columnspan=2, pady=10, padx=15, sticky="ew")

        self.import_data = ttk.Button(self.root, text="Import Data File", command=self.on_upload)
        self.import_data.grid(column=0, row=2, columnspan=2, pady=10, padx=15, sticky="ew")

        self.status_label = ttk.Label(self.root, text="Ready", foreground="green", font=("Helvetica", 12))
        self.status_label.grid(column=0, row=3, columnspan=2, pady=10, sticky="s")

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)


def main():
    root = tk.Tk()
    Tj_analyser(root)
    root.mainloop()

if __name__ == "__main__":
    main()
