import pyperclip

# مپ کیبورد QWERTY به فارسی استاندارد
mapping = {
    'q': 'ض', 'w': 'ص', 'e': 'ث', 'r': 'ق', 't': 'ف',
    'y': 'غ', 'u': 'ع', 'i': 'ه', 'o': 'خ', 'p': 'ح', '[': 'ج', ']': 'چ',
    'a': 'ش', 's': 'س', 'd': 'ی', 'f': 'ب', 'g': 'ل', 'h': 'ا', 'j': 'ت',
    'k': 'ن', 'l': 'م', ';': 'ک', "'": 'گ',
    'z': 'ظ', 'x': 'ط', 'c': 'ز', 'v': 'ر', 'b': 'ذ', 'n': 'د', 'm': 'پ',
    ',': 'و', '?': '؟', ' ': ' '
}

# گرفتن متن از کلیپ‌بورد
original_text = pyperclip.paste()

# تبدیل کاراکترها
converted_text = ''.join(mapping.get(ch, ch) for ch in original_text)

# ذخیره در کلیپ‌بورد
pyperclip.copy(converted_text)

print("📋 متن دریافتی از کلیپ‌بورد:", original_text)
print("✅ متن تبدیل‌شده:", converted_text)
print("✅ متن تبدیل‌شده اکنون در کلیپ‌بورد آماده چسباندن است.")
