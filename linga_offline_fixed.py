import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip
import json
import os
import re

CONFIG_FILE = "keyboard_map.json"

# مپ پیش‌فرض انگلیسی→فارسی
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

# مپ معکوس فارسی→انگلیسی
reverse_mapping = {v: k for k, v in mapping.items()}

def save_mapping():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

def detect_language(text):
    persian_chars = len(re.findall(r'[آ-یءۀچپژگ]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    return 'fa' if persian_chars > english_chars else 'en'

def is_finglish(text):
    # متن فقط با حروف انگلیسی و فاصله و علائم ساده باشد
    return bool(re.fullmatch(r"[a-zA-Z0-9\s.,!?'\-:;]*", text))

def perform_conversion(text):
    lang = detect_language(text)
    if lang == 'en':
        if is_finglish(text):
            status_var.set("⚠️ متن قاطی نیست، فینگلیش است.")
        converted = ''.join(mapping.get(ch, ch) for ch in text)
    else:
        converted = ''.join(reverse_mapping.get(ch, ch) for ch in text)
    return converted

def convert_text():
    text = input_box.get("1.0", tk.END).rstrip("
")
    converted = perform_conversion(text)
    output_box.delete("1.0", tk.END)
    output_box.insert("1.0", converted)
    pyperclip.copy(converted)
    status_var.set(status_var.get() + " ✅ متن تبدیل و در کلیپ‌بورد کپی شد.")

def paste_clipboard():
    try:
        text = pyperclip.paste()
        input_box.delete("1.0", tk.END)
        input_box.insert("1.0", text)
        converted = perform_conversion(text)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", converted)
        pyperclip.copy(converted)
        if not status_var.get():
            status_var.set("📋 متن از کلیپ‌بورد اضافه و تبدیل شد.")
        else:
            status_var.set(status_var.get() + " 📋 Paste و تبدیل انجام شد.")
    except:
        status_var.set("❌ خطا در خواندن کلیپ‌بورد")

def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)
    status_var.set("")

def edit_mapping():
    key = simpledialog.askstring("ویرایش کلید", "حرف کیبورد را وارد کن:")
    if not key:
        return
    val = simpledialog.askstring("ویرایش خروجی", f"حرف فارسی برای '{key}' را وارد کن:")
    if val is None:
        return
    mapping[key] = val
    save_mapping()
    global reverse_mapping
    reverse_mapping = {v: k for k, v in mapping.items()}
    messagebox.showinfo("ذخیره شد", f"برای '{key}' معادل '{val}' ذخیره شد.")

def make_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="کپی", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="پیست", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="انتخاب همه", command=lambda: widget.event_generate("<<SelectAll>>"))
    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)
    widget.bind("<Button-3>", show_menu)

# رابط کاربری
root = tk.Tk()
root.title("تبدیل کیبورد دوطرفه با تشخیص فینگلیش - پرتابل (ایده از مصطفی رئوفی و GapGPT)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.BOTH, expand=True)

tk.Label(frame, text="ورودی:").grid(row=0, colum, sticky="w")
input_box = tk.Text(frame, height=5, width
