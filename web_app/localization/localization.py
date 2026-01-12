# Import standard library modules for JSON handling and file system operations
import json
import os

class Translator:
    """
    Multi-language translation manager for internationalization (i18n) support.
    Handles loading, caching, and retrieving translated text from JSON language files.
    """
    
    def __init__(self, lang="en"):
        """
        Initialize the translator with a default language.
        
        Args:
            lang (str): Language code (e.g., 'en', 'fr', 'de'). Defaults to English.
        """
        # Get the absolute path of the localization directory
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Store current language preference
        self.lang = lang
        
        # Initialize empty dictionary to store translation key-value pairs
        self.translations = {}
        
        # Load initial translations for the specified language
        self.load_translations(lang)

    def load_translations(self, lang):
        """
        Load translation data from a JSON file for the specified language.
        
        Args:
            lang (str): Language code to load translations for
        
        Expected file format: {lang}.json (e.g., en.json, fr.json)
        File should contain key-value pairs: {"key": "translated_text"}
        """
        # Construct path to language-specific JSON file
        path = os.path.join(self.base_path, f"{lang}.json")
        
        try:
            # Open and parse JSON translation file with UTF-8 encoding
            with open(path, encoding='utf-8') as jsonfile:
                self.translations = json.load(jsonfile)
        except FileNotFoundError:
            # Gracefully handle missing language files by using empty translations
            # This prevents crashes when requested language files don't exist
            self.translations = {}
            print(f"Warning: Translation file '{lang}.json' not found. Using fallback.")

    def set_language(self, lang):
        """
        Change the current language and reload translations.
        
        Args:
            lang (str): New language code to switch to
        
        This method allows dynamic language switching during runtime.
        """
        # Update current language setting
        self.lang = lang
        
        # Load translations for the new language
        self.load_translations(lang)

    def t(self, key):
        """
        Translate a given key to the current language.
        
        Args:
            key (str): Translation key to look up
            
        Returns:
            str: Translated text if key exists, otherwise returns the key itself as fallback
            
        The fallback behavior ensures the application continues to function
        even with missing translations, displaying the key instead of crashing.
        """
        return self.translations.get(key, key)

# --- File Structure Expected ---
# localization/
# ├── localization.py (this file)
# ├── en.json (English translations)
# ├── fr.json (French translations)
# └── de.json (German translations, etc.)