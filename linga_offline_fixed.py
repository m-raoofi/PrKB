import py_compile

code = r'''
import tkinter as tk
from tkinter import scrolledtext
import json
import os
import pyperclip

# نگاشت کیبورد انگلیسی به فارسی
eng_to_fa = {
    'a': 'ش', 'b': 'ذ', 'c': 'ز', 'd': 'ی', 'e': 'ث',
    'f': 'ب', 'g': 'ل', 'h': 'ا', 'i': 'هـ', 'j': 'ت',
    'k': 'ن', 'l': 'م', 'm': 'پ', 'n': 'د', 'o': 'خ',
    'p': 'ح', 'q': 'ض', 'r': 'ق', 's': 'س', 't': 'ف',
    'u': 'ع', 'v': 'ر', 'w': 'ص', 'x': 'ط', 'y': 'غ', 'z': 'ظ',
    'A': 'ِ', 'B': 'ذ', 'C': 'ژ', 'D': 'ي', 'E': 'َ',
    'F': 'ً', 'G': 'ُ', 'H': 'آ', 'I': '—', 'J': 'ة',
    'K': '»', 'L': '«', 'M': 'ٱ', 'N': '،', 'O': ']',
    'P': '[', 'Q': 'ْ', 'R': 'ٌ', 'S': 'ٍ', 'T': '؛',
    'U': ']', 'V': 'ـ', 'W': '}', 'X': '{', 'Y': 'ى', 'Z': 'ؤ'
}

# برعکس‌سازی مپ برای فارسی به انگلیسی
fa_to_eng = {v: k for k, v in eng_to_fa.items()}

SAVE_FILE = 'saved_text.json'

def save_text(input_text, output_text):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'input': input_text, 'output': output_text}, f, ensure_ascii=False, indent=2)

def load_text():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('input', ''), data.get('output', '')
    return '', ''

def convert_text(text):
    # تشخیص خودکار زبان
    if all(ch in eng_to_fa or not ch.isalpha() for ch in text):
        return ''.join(eng_to_fa.get(ch, ch) for ch in text)
    else:
        return ''.join(fa_to_eng.get(ch, ch) for ch in text)

def paste_clipboard():
    try:
        return pyperclip.paste().rstrip("\n")
    except:
        return ''

# رابط کاربری
root = tk.Tk()
root.title("Linga Offline AutoSave")

input_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)

input_box.grid(row=0, column=0, padx=10, pady=10)
output_box.grid(row=0, column=1, padx=10, pady=10)

def on_convert():
    text = input_box.get("1.0", tk.END).rstrip("\n")
    converted = convert_text(text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, converted)
    save_text(text, converted)

def on_paste():
    text = paste_clipboard()
    input_box.delete("1.0", tk.END)
    input_box.insert(tk.END, text)
    on_convert()

convert_btn = tk.Button(root, text="تبدیل", command=on_convert)
paste_btn = tk.Button(root, text="پیست", command=on_paste)

convert_btn.grid(row=1, column=0, pady=5)
paste_btn.grid(row=1, column=1, pady=5)

# لود خودکار
inp, outp = load_text()
input_box.insert(tk.END, inp)
output_box.insert(tk.END, outp)

root.mainloop()
'''

file_path = '/mnt/data/linga_offline_autosave.py'
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)

# تست SyntaxError
py_compile.compile(file_path, doraise=True)
file_path
