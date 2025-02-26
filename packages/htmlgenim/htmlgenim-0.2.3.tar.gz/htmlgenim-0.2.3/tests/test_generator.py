import unittest
from htmlgenim.generator import HTMLGenerator

class TestHTMLGenerator(unittest.TestCase):
    def test_render(self):
        template = "<h1>{{ title }}</h1>"
        generator = HTMLGenerator(template)
        result = generator.render(title="Тест")
        self.assertEqual(result, "<h1>Тест</h1>")

    def test_save_to_file(self):
        template = "<p>{{ content }}</p>"
        generator = HTMLGenerator(template)
        html_content = generator.render(content="Сохраняем в файл")
        generator.save_to_file(html_content, "test_output.html")
        with open("test_output.html", "r", encoding="utf-8") as file:
            content = file.read()
        self.assertEqual(content, "<p>Сохраняем в файл</p>")

if __name__ == "__main__":
    unittest.main()