import tkinter as tk
import pyperclip
import json
import os

# ----------------------------
# تنظیمات و نقشه کیبورد
# ----------------------------
keyboard_map = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ',
    # حروف بزرگ
    'Q': 'َ', 'W': 'ٌ', 'E': 'ُ', 'R': 'ً', 'T': 'ِ', 'Y': 'ٍ', 'U': ']', 'I': '[', 'O': '}', 'P': '{',
    'A': 'ؤ', 'S': 'ئ', 'D': 'ي', 'F': 'إ', 'G': 'أ', 'H': 'آ', 'J': 'ة', 'K': '»', 'L': '«',
    'Z': 'ك', 'X': 'ٓ', 'C': 'ژ', 'V': 'ٔ', 'B': 'ء', 'N': '‌', 'M': 'ء'
}

reverse_map = {v: k for k, v in keyboard_map.items()}

SAVE_FILE = "saved_text.json"

# ----------------------------
# توابع نگاشت دوطرفه
# ----------------------------
def convert_text(text):
    if sum(ch in keyboard_map for ch in text) >= sum(ch in reverse_map for ch in text):
        return ''.join(keyboard_map.get(ch, ch) for ch in text)
    else:
        return ''.join(reverse_map.get(ch, ch) for ch in text)

# ----------------------------
# رویدادها و دکمه‌ها
# ----------------------------
def on_convert():
    text = input_box.get("1.0", tk.END).rstrip("\n")
    converted = convert_text(text)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, converted)
    pyperclip.copy(converted)
    save_text(text)

def on_clear():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)

def on_paste(event=None):
    try:
        pasted = pyperclip.paste()
        input_box.insert(tk.END, pasted)
    except Exception:
        pass
    return "break"

def save_text(text):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump({"text": text}, f, ensure_ascii=False)
    except Exception:
        pass

def load_text():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "text" in data:
                    input_box.delete("1.0", tk.END)
                    input_box.insert(tk.END, data["text"])
        except Exception:
            pass

# ----------------------------
# ساخت رابط کاربری
# ----------------------------
root = tk.Tk()
root.title("تبدیل کیبورد فارسی–QWERTY (ایده از مصطفی رئوفی و GapGPT)")

# قاب متون
input_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)
output_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)

# اتصال Paste با ماوس و Ctrl+V
input_box.bind("<Control-v>", on_paste)
input_box.bind("<Button-3>", lambda e: on_paste())

# قاب دکمه‌ها
btn_convert = tk.Button(root, text="تبدیل", command=on_convert)
btn_clear = tk.Button(root, text="پاک کردن متن", command=on_clear)

# جایگذاری
input_box.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
output_box.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
btn_convert.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
btn_clear.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# بارگذاری خودکار متن ذخیره شده
load_text()

root.mainloop()
