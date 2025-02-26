import re
import os

class HTMLGenerator:
    def __init__(self, template):
        self.template = template

    def render(self, **context):
        # Заменяем переменные в шаблоне на значения из контекста
        def replace_match(match):
            key = match.group(1).strip()  # Убираем лишние пробелы
            return str(context.get(key, f"{{{{ {key} }}}}"))  # Если ключ не найден, оставляем как есть

        # Используем регулярное выражение для поиска переменных в шаблоне
        pattern = r"\{\{\s*(\w+)\s*\}\}"  # Ищем {{ key }} с возможными пробелами вокруг key
        rendered_html = re.sub(pattern, replace_match, self.template)
        return rendered_html

    @staticmethod
    def save_to_file(html_content, output_file):
        # Получаем абсолютный путь к файлу
        output_path = os.path.abspath(output_file)
        # Создаем директорию, если её нет
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Сохраняем файл
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Файл успешно сохранен: {output_path}")