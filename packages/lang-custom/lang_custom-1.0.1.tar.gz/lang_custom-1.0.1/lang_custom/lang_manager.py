import os
import json

class LangManager:
    def __init__(self):
        self.config_path = self.find_config_file()
        if not self.config_path:
            raise FileNotFoundError("config_lang.json not found in the project root directory.")
        
        self.lang_dir = None
        self.default_lang = "en"
        self.lang_cache = {}
        self.load_config()

    def find_config_file(self):
        """Automatically find config_lang.json in the project root directory"""
        project_root = os.getcwd()
        config_path = os.path.join(project_root, "config_lang.json")
        return config_path if os.path.exists(config_path) else None

    def load_config(self):
        """Read the config file to get the Lang directory path"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file '{self.config_path}' does not exist.")

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                self.lang_dir = config.get("lang_path")

                if not self.lang_dir or not os.path.isdir(self.lang_dir):
                    raise ValueError(f"Invalid or missing 'lang_path' in '{self.config_path}'.")

        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in '{self.config_path}'.")

    def set_config_path(self, path):
        """Allows users to change the config file dynamically"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file '{path}' not found.")
        
        self.config_path = path
        self.load_config()

    def load_lang(self, lang):
        """Load a language file"""
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

    def get(self, lang, key, default=None):
        """Retrieve a translated string"""
        data = self.load_lang(lang)
        keys = key.split(".")
        for k in keys:
            if not isinstance(data, dict):
                return default
            data = data.get(k, default)
        return data

lang_manager = LangManager()

def set_config(path):
    """Allow users to set a new config file"""
    lang_manager.set_config_path(path)

def get(lang, key, default=None):
    """Retrieve a translation"""
    return lang_manager.get(lang, key, default)
