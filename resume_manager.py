import os
import uuid
import json
import shutil
import subprocess
import platform
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

CONFIG_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.json")
with open(CONFIG_FILE, "r") as f:
    CONFIG = json.load(f)

APP_DIR = os.path.join(os.path.expanduser("~"), ".resume_app_storage")
INDEX_FILE = os.path.join(APP_DIR, "index.json")
EXT = CONFIG["file_extension"].lstrip('.')
TARGET_NAME = CONFIG["target_name"] + CONFIG["file_extension"]
DOWNLOADS_DIR = os.path.expanduser(CONFIG.get("download_folder", "~/Downloads"))

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

def upload_files():
    files = filedialog.askopenfilenames(
        title=f"Select {EXT.upper()} file(s)",
        filetypes=[(EXT.upper(), f"*{CONFIG['file_extension']}")]
    )
    if not files:
        return
    idx = load_index()
    for path in files:
        name = os.path.basename(path)
        uid = str(uuid.uuid4())
        dest = os.path.join(APP_DIR, uid + CONFIG['file_extension'])
        shutil.copy2(path, dest)
        idx.append({"id": uid, "name": name})
    save_index(idx)
    refresh_list()


def download_selected():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Please select a file.")
        return
    idx = load_index()
    item = idx[sel[0]]
    src = os.path.join(APP_DIR, item["id"] + CONFIG['file_extension'])
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


def delete_selected():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning("No selection", "Please select a file to delete.")
        return
    idx = load_index()
    item = idx.pop(sel[0])
    filepath = os.path.join(APP_DIR, item["id"] + CONFIG['file_extension'])
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass
    save_index(idx)
    refresh_list()
    messagebox.showinfo("Deleted", f"Removed {item['name']} from storage.")


def open_settings():
    try:
        if os.name == 'nt':
            os.startfile(CONFIG_FILE)
        elif platform.system() == 'Darwin':
            subprocess.call(['open', CONFIG_FILE])
        else:
            subprocess.call(['xdg-open', CONFIG_FILE])
    except Exception as e:
        messagebox.showerror('Error', f'Cannot open settings:\n{e}')


root = tk.Tk()
root.title("File Manager")
root.minsize(500, 300)

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

btn_frame = ttk.Frame(main_frame)
btn_frame.pack(fill=tk.X, pady=(0, 10))

upload_btn = ttk.Button(btn_frame, text=f"Upload {EXT.upper()} file(s)", command=upload_files)
upload_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

download_btn = ttk.Button(btn_frame, text=f"Download as {TARGET_NAME}", command=download_selected)
download_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

delete_btn = ttk.Button(btn_frame, text="Delete Selected", command=delete_selected)
delete_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

settings_btn = ttk.Button(btn_frame, text="Settings", command=open_settings)
settings_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

list_frame = ttk.Frame(main_frame)
list_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=(None, 12))
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox.yview)


def refresh_list():
    listbox.delete(0, tk.END)
    for entry in load_index():
        listbox.insert(tk.END, entry["name"])

refresh_list()
root.mainloop()
