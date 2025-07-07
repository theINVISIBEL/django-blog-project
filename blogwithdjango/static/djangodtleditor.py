import os
import re

TEMPLATE_DIR = 'templates'  # ← غيّره إذا كنت تضع ملفات HTML في مكان آخر

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # أضف {% load static %} في الأعلى إذا لم يكن موجوداً
    if '{% load static %}' not in content:
        content = '{% load static %}\n' + content

    # استبدال src="..." (مثل <script>, <img>, <iframe>...)
    content = re.sub(
        r'(\ssrc=["\'])(?!\{%\s*static)([^"\']+)(["\'])',
        r'\1{% static "\2" %}\3',
        content
    )

    # استبدال href="..." (مثل <link>, <a>...)
    content = re.sub(
        r'(\shref=["\'])(?!\{%\s*static)([^"\']+)(["\'])',
        r'\1{% static "\2" %}\3',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"✅ تم تعديل الملف: {filepath}")

def process_all_templates():
    for root, _, files in os.walk(TEMPLATE_DIR):
        for name in files:
            if name.endswith('.html'):
                path = os.path.join(root, name)
                process_html_file(path)

if __name__ == '__main__':
    process_all_templates()
    print("\n🎯 تم استبدال كل روابط src و href بنجاح.")

