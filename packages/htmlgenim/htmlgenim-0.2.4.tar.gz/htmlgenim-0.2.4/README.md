# HTML Generator

Простой генератор HTML-страниц на Python. Позволяет создавать HTML-файлы на основе шаблонов и данных.

## Установка

Установите библиотеку через pip:

```bash
pip install htmlgenim
```

## Использование
```bash
from htmlgenim.generator import HTMLGenerator

# Шаблон HTML с переменными
template = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    <p>{{ content }}</p>
</body>
</html>
"""

# Данные для подстановки
data = {
    "title": "Моя страница",
    "heading": "Привет, мир!",
    "content": "Это пример использования HTML генератора."}

# Генерация HTML
generator = HTMLGenerator(template)
html_content = generator.render(**data)

# Сохранение файла в текущей директории
generator.save_to_file(html_content, "output.html")
```