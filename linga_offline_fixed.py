import tkinter as tk
import pyperclip

# Map English QWERTY to Persian
mapping = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف', 'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت', 'k': 'ن', 'l': 'م',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ',
    'Q': 'َ', 'W': 'ِ', 'E': 'é', 'R': 'ق', 'T': '‌', 'Y': 'ّ', 'U': 'ئ', 'I': 'إ', 'O': 'ؤ', 'P': 'ء',
    'A': 'آ', 'S': 'ً', 'D': 'ٌ', 'F': 'ٍ', 'G': '»،', 'H': '«', 'J': 'ة', 'K': 'ٱ', 'L': 'ﷲ',
    'Z': 'ژ', 'X': 'ٔ', 'C': 'چ', 'V': 'ء', 'B': '…', 'N': '٬', 'M': '؟'
}

reverse_mapping = {v: k for k, v in mapping.items()}

def convert_text(text):
    result = ""
    # Detect Persian proportion
    persian_chars = sum(1 for ch in text if '\u0600' <= ch <= '\u06FF')
    english_chars = sum(1 for ch in text if 'a' <= ch.lower() <= 'z')
    if persian_chars >= english_chars:
        # Persian to English
        for ch in text:
            result += reverse_mapping.get(ch, ch)
    else:
        # English to Persian
        for ch in text:
            result += mapping.get(ch, ch)
    return result

def do_convert():
    text = input_box.get("1.0", tk.END).rstrip("\n")
    output_box.delete("1.0", tk.END)
    converted = convert_text(text)
    output_box.insert(tk.END, converted)

def do_paste_and_convert():
    try:
        text = pyperclip.paste()
        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, text)
        do_convert()
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Clipboard error: {e}")

def do_copy():
    try:
        text = output_box.get("1.0", tk.END).rstrip("\n")
        pyperclip.copy(text)
    except Exception as e:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Clipboard error: {e}")

def clear_text():
    input_box.delete("1.0", tk.END)
    output_box.delete("1.0", tk.END)

root = tk.Tk()
root.title("Persian–QWERTY Keyboard Converter (Offline)")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# line 114 fixed
tk.Label(frame, text="\u0648\u0631\u0648\u062f\u06cc:").grid(row=0, column=0, sticky="w")
input_box = tk.Text(frame, width=60, height=5)
input_box.grid(row=1, column=0, columnspan=3, pady=5)

tk.Label(frame, text="\u062E\u0631\u0648\u062C\u06CC:").grid(row=2, column=0, sticky="w")
output_box = tk.Text(frame, width=60, height=5)
output_box.grid(row=3, column=0, columnspan=3, pady=5)

btn_convert = tk.Button(frame, text="تبدیل", command=do_convert)
btn_convert.grid(row=4, column=0, pady=5, sticky="we")

btn_paste = tk.Button(frame, text="Paste + Convert", command=do_paste_and_convert)
btn_paste.grid(row=4, column=1, pady=5, sticky="we")

btn_copy = tk.Button(frame, text="Copy Output", command=do_copy)
btn_copy.grid(row=4, column=2, pady=5, sticky="we")

btn_clear = tk.Button(frame, text="پاک کردن متن", command=clear_text)
btn_clear.grid(row=5, column=0, columnspan=3, pady=5, sticky="we")

tk.Label(frame, text="ایده از مصطفی رئوفی و GapGPT").grid(row=6, column=0, columnspan=3, pady=5)

root.mainloop()
