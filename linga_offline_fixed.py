import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip
import json
import os

CONFIG_FILE = "keyboard_map.json"

# مپ پیش‌فرض کیبورد
default_mapping = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف',
    'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح', '[': 'ج', ']': 'چ',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت',
    'k': 'ن', 'l': 'م', ';': 'ک', "'": 'گ',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ',
    ',': 'و', '?': '؟', ' ': ' '
}

# بارگذاری یا ایجاد تنظیمات
if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            mapping = json.load(f)
    except:
        mapping = default_mapping.copy()
else:
    mapping = default_mapping.copy()

# ذخیره تنظیمات
def save_mapping():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

# تابع تبدیل متن
def convert_text():
    text = input_box.get("1.0", tk.END).rstrip("\n")
    converted = ''.join(mapping.get(ch, ch) for ch in text)
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", converted)
    pyperclip.copy(converted)
    status_var.set("✅ متن تبدیل و در کلیپ‌بورد کپی شد.")

# خواندن از کلیپ‌بورد
def paste_clipboard():
    text = pyperclip.paste()
    input_box.delete("1.0", tk.END)
    input_box.insert("1.0", text)
    status_var.set("📋 متن از کلیپ‌بورد اضافه شد.")

# پاک‌کردن جعبه‌های متن
def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    status_var.set("")

# ویرایش مپ کیبورد
def edit_mapping():
    key = simpledialog.askstring("ویرایش کلید", "حرف کیبورد را وارد کن:")
    if not key:
        return
    val = simpledialog.askstring("ویرایش خروجی", f"حرف فارسی برای '{key}' را وارد کن:")
    if val is None:
        return
    mapping[key] = val
    save_mapping()
    messagebox.showinfo("ذخیره شد", f"برای '{key}' معادل '{val}' ذخیره شد.")

# ساخت رابط کاربری
root = tk.Tk()
root.title("تبدیل کیبورد فارسی - پرتابل")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="ورودی:").grid(row=0, column=0, sticky="w")
input_box = tk.Text(frame, height=5, width=60)
input_box.grid(row=1, column=0, columnspan=3, pady=5)

tk.Label(frame, text="خروجی:").grid(row=2, column=0, sticky="w")
output_box = tk.Text(frame, height=5, width=60)
output_box.grid(row=3, column=0, columnspan=3, pady=5)

tk.Button(frame, text="📋 Paste", command=paste_clipboard).grid(row=4, column=0, pady=5, sticky="ew")
tk.Button(frame, text="🔄 تبدیل", command=convert_text).grid(row=4, column=1, pady=5, sticky="ew")
tk.Button(frame, text="🗑 پاک‌کردن", command=clear_text).grid(row=4, column=2, pady=5, sticky="ew")

tk.Button(frame, text="⚙ ویرایش مپ کیبورد", command=edit_mapping).grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

status_var = tk.StringVar()
tk.Label(frame, textvariable=status_var, fg="green").grid(row=6, column=0, columnspan=3, sticky="w")

root.mainloop()
