import json
import os

class Translator:
    def __init__(self, lang="en"):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.lang = lang
        self.translations = {}
        self.load_translations(lang)

    def load_translations(self, lang):
        path = os.path.join(self.base_path, f"{lang}.json")
        try:
            with open(path, encoding='utf-8') as jsonfile:
                self.translations = json.load(jsonfile)
        except FileNotFoundError:
            self.translations = {}

    def set_language(self, lang):
        self.lang = lang
        self.load_translations(lang)

    def t(self, key):
        return self.translations.get(key, key)

