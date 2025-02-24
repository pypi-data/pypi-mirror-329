import json
import os

class FashionWords:
    def __init__(self):
        self.words = self.load_words()

    def load_words(self):
        path = os.path.join(os.path.dirname(__file__), "categories.json")
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_all_words(self):
        """Retorna todas as palavras de moda disponíveis"""
        return [word for category in self.words.values() for word in category]

    def get_by_category(self, category):
        """Retorna palavras de uma categoria específica"""
        return self.words.get(category, [])
