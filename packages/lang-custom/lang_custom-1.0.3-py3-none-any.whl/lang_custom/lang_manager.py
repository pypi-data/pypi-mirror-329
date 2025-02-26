import os
import json

class LangManager:
    def __init__(self):
        self.lang_dir = self.find_or_create_lang_dir()
        self.default_lang = "en"
        self.lang_cache = {}
        self.selected_group = None

    def find_or_create_lang_dir(self):
        project_root = os.getcwd()
        lang_path = os.path.join(project_root, "Lang_data")

        if not os.path.exists(lang_path):
            os.makedirs(lang_path)  # Tạo thư mục nếu không tồn tại
            self.create_default_lang_file(lang_path)

        return lang_path

    def create_default_lang_file(self, lang_path):
        default_data = {
            "name1": {
                "example": "text",
                "example2": "text2"
            },
            "name2": {
                "example": "text",
                "example2": "text2"
            }
        }
        en_path = os.path.join(lang_path, "en.json")
        with open(en_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)

    def load_lang(self, lang):
        if lang in self.lang_cache:
            return self.lang_cache[lang]

        lang_path = os.path.join(self.lang_dir, f"{lang}.json")
        if not os.path.exists(lang_path):
            raise FileNotFoundError(f"Language file '{lang}.json' not found in '{self.lang_dir}'.")

        try:
            with open(lang_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.lang_cache[lang] = data
                return data
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in '{lang_path}'.")

    def set(self, group_name):
        self.selected_group = group_name

    def get(self, lang, key, default=None):
        if not self.selected_group:
            raise ValueError("No language group selected. Use 'set(group_name)' first.")

        data = self.load_lang(lang)
        group_data = data.get(self.selected_group, {})

        return group_data.get(key, default)

lang_manager = LangManager()

def set(group_name):
    lang_manager.set(group_name)

def get(lang, key, default=None):
    return lang_manager.get(lang, key, default)
