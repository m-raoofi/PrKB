# نسخهٔ نهایی دو زبانه با تشخیص خودکار و بدون SyntaxError

import tkinter as tk
import json
import os
import pyperclip

# ---------- مپ کیبورد دوطرفه ----------
key_map_en_to_fa = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    'z': 'ئ', 'x': 'ء', 'c': 'ؤ', 'v': 'ر', 'b': 'لا', 'n': 'ى', 'm': 'و'
}

# مپ معکوس فارسی → انگلیسی
key_map_fa_to_en = {v: k for k, v in key_map_en_to_fa.items()}

# ---------- توابع تبدیل ----------

def convert_english_to_persian(text):
    return ''.join(key_map_en_to_fa.get(ch.lower(), ch) for ch in text)

def convert_persian_to_english(text):
    return ''.join(key_map_fa_to_en.get(ch, ch) for ch in text)

# تشخیص خودکار زبان ورودی
def detect_and_convert(text):
    persian_count = sum('\u0600' <= ch <= '\u06FF' for ch in text)
    latin_count = sum('a' <= ch.lower() <= 'z' for ch in text)
    if persian_count > latin_count:
        return convert_persian_to_english(text)
    else:
        return convert_english_to_persian(text)

# ---------- مدیریت ذخیره/بارگذاری ----------
SAVE_FILE = 'saved_text.json'

def save_text(content):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'text': content}, f, ensure_ascii=False, indent=2)

def load_text():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('text', '')
    return ''

# ---------- رابط کاربری ----------
root = tk.Tk()
root.title("تبدیل‌گر کیبورد دو زبانه")

input_text = tk.Text(root, height=10, width=50)
input_text.pack()
output_text = tk.Text(root, height=10, width=50)
output_text.pack()

def do_convert():
    txt = input_text.get("1.0", tk.END).rstrip("\n")
    result = detect_and_convert(txt)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    save_text(txt)

def paste_and_convert():
    try:
        txt = pyperclip.paste()
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, txt)
        do_convert()
    except:
        pass

tk.Button(root, text="تبدیل", command=do_convert).pack()
tk.Button(root, text="Paste + تبدیل", command=paste_and_convert).pack()

# لود خودکار متن قبلی
prev = load_text()
if prev:
    input_text.insert(tk.END, prev)
    do_convert()

root.mainloop()
