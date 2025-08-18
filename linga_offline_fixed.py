import tkinter as tk
import pyperclip
import json
import os

SAVE_FILE = "saved_text.json"
MAP_FILE = "keyboard_map.json"

default_map = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ',
    'Q': 'َ', 'W': 'ٌ', 'E': 'ُ', 'R': 'ً', 'T': 'ِ', 'Y': 'ٍ', 'U': ']', 'I': '[', 'O': '}', 'P': '{',
    'A': 'ؤ', 'S': 'ئ', 'D': 'ي', 'F': 'إ', 'G': 'أ', 'H': 'آ', 'J': 'ة', 'K': '»', 'L': '«',
    'Z': 'ك', 'X': 'ٓ', 'C': 'ژ', 'V': 'ٔ', 'B': 'ء', 'N': '‌', 'M': 'ء'
}

def load_map():
    if os.path.exists(MAP_FILE):
        try:
            with open(MAP_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default_map

def save_map(current_map):
    try:
        with open(MAP_FILE, "w", encoding="utf-8") as f:
            json.dump(current_map, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

keyboard_map = load_map()
reverse_map = {v: k for k, v in keyboard_map.items()}

def convert_text(text):
    if sum(ch in keyboard_map for ch in text) >= sum(ch in reverse_map for ch in text):
        return ''.join(keyboard_map.get(ch, ch) for ch in text)
    else:
        return ''.join(reverse_map.get(ch, ch) for ch in text)

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

def on_save_map():
    save_map(keyboard_map)

root = tk.Tk()
root.title("تبدیل کیبورد فارسی–QWERTY (ایده از مصطفی رئوفی  )")

input_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)
output_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)

input_box.bind("<Control-v>", on_paste)
input_box.bind("<Button-3>", lambda e: on_paste())

btn_convert = tk.Button(root, text="تبدیل", command=on_convert)
btn_clear = tk.Button(root, text="پاک کردن متن", command=on_clear)
btn_save_map = tk.Button(root, text="ذخیره مپ کیبورد", command=on_save_map)

input_box.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
output_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
btn_convert.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
btn_clear.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
btn_save_map.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

load_text()

root.mainloop()
