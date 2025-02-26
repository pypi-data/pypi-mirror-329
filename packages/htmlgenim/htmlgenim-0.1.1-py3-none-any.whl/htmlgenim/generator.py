import re

class HTMLGenerator:
    def __init__(self, template):
        self.template = template

    def render(self, **context):
        # Заменяем переменные в шаблоне на значения из контекста
        def replace_match(match):
            key = match.group(1)
            return str(context.get(key, ""))

        # Используем регулярное выражение для поиска переменных в шаблоне
        pattern = r"\{\{(\w+)\}\}"
        rendered_html = re.sub(pattern, replace_match, self.template)
        return rendered_html

    @staticmethod
    def save_to_file(html_content, output_file):
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(html_content)