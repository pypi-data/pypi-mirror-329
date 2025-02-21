import json
import os
from pathlib import Path
import logging




def set_locale(language: str):
    if PIntl.instance:
        PIntl.instance.set_locale(language)

def _(key: str, params: dict = {}):
    if PIntl.instance:
        return PIntl.instance.get_string(key, params=params)
    else:
        raise Exception('No Intl instance found')


class PIntl:
    instance = None
    @staticmethod 
    def load(folderPath: str, default_lang='en'):
        translations = {}
        
        for filename in os.listdir(folderPath):
            if filename.endswith('.arb'):
                with open(os.path.join(folderPath, filename)) as file:
                    lang = Path(filename).stem.split('_')[-1]
                    translations[lang]=json.load(file)
                    logging.info(f'Loaded {lang} translations')

        retval = PIntl(default_lang, default_lang=default_lang, translations=translations)
        return retval


    def __init__(self, language: str, default_lang='en', translations={}):
        self.language = language
        self.default_lang = default_lang
        self.translations = translations
        # Set the last instance to this instance
        PIntl.instance = self

    def fill_in_params(self, string: str, param_defs: dict, params: dict):
        # For now, no neet to see param_defs. Later when more complicated params are available, we might need to use it.
        for key in params:
            key_match = f'{{{key}}}'
            string = string.replace(key_match, str(params[key]))
        return string

    def get_string(self, key: str, params: dict = {}):
        if key in self.translations[self.language]:
            string = self.translations[self.language][key]
            param_defs = {}
            if "@"+key in self.translations[self.language]:
                param_defs = self.translations[self.language]["@"+key]
            return self.fill_in_params(self.translations[self.language][key], param_defs=param_defs, params=params)
        else:
            return f'##{key}##'

    def set_locale(self, language: str):
        if not language:
            self.language = self.default_lang
            return

        languages = self.translations.keys()

        # some environments, like flutter, use language code separated by underscore instead of dash
        language = language.replace('_', '-')
        
        # exact match
        if language in languages:
            self.language = language
            return

        # match with language code first part
        
        primary_language = language.split('-')[0]
        for lang in languages:
            if lang.split('-')[0] == primary_language:
                self.language = lang
                return

        # no match, use default
        self.language = self.default_lang

    