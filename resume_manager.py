import os
import uuid
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

#config
APP_DIR = os.path.join(os.path.expanduser("~"), ".resume_app_storage")
INDEX_FILE = os.path.join(APP_DIR, "index.json")
DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
TARGET_NAME = "arnav_kalekar_resume.pdf"

os.makedirs(APP_DIR, exist_ok=True)
if not os.path.exists(INDEX_FILE):
    with open(INDEX_FILE, "w") as f:
        json.dump([], f)

def load_index():
    with open(INDEX_FILE, "r") as f:
        return json.load(f)

def save_index(idx):
    with open(INDEX_FILE, "w") as f:
        json.dump(idx, f, indent=2)

def upload_pdfs():
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF", "*.pdf")]
    )
    if not files:
        return
    idx = load_index()
    for path in files:
        name = os.path.basename(path)
        uid = str(uuid.uuid4())
        dest = os.path.join(APP_DIR, uid + ".pdf")
        shutil.copy2(path, dest)
        idx.append({"id": uid, "name": name})
    save_index(idx)
    refresh_list()

def download_selected():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Please select a PDF.")
        return
    idx = load_index()
    item = idx[sel[0]]
    src = os.path.join(APP_DIR, item["id"] + ".pdf")
    dst = os.path.join(DOWNLOADS_DIR, TARGET_NAME)
    # Delete existing
    if os.path.exists(dst):
        try:
            os.remove(dst)
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete existing file:\n{e}")
            return
    # Copy new
    try:
        shutil.copy2(src, dst)
        messagebox.showinfo("Done", f"Downloaded as:\n{dst}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not copy file:\n{e}")

def refresh_list():
    listbox.delete(0, tk.END)
    for entry in load_index():
        listbox.insert(tk.END, entry["name"])

root = tk.Tk()
root.title("Resume Manager")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

btn_upload = tk.Button(frame, text="Upload PDF(s)", command=upload_pdfs)
btn_upload.pack(fill=tk.X, pady=(0,10))

listbox = tk.Listbox(frame, height=10)
listbox.pack(fill=tk.BOTH, expand=True)

btn_download = tk.Button(frame, text="Download as arnav_kalekar_resume.pdf", command=download_selected)
btn_download.pack(fill=tk.X, pady=(10,0))

refresh_list()
root.mainloop()
