import os
import re
from abc import ABC, abstractmethod

from ..conf import get_global_config


class LexicalAnalyzer:
    #keywords_pattern = re.compile(r'\b(int|float|bool|if|then|else|for|to|do|while|read|write|true|false|end|program|var)\b', re.VERBOSE)
    #delimiter_pattern = re.compile(r'(NE|EQ|LT|LE|GT|GE|\+|-|\*|\/|and|or|\~|;|:|,|\{|\}|\(|\)|\.)', re.VERBOSE)
    #number_pattern = re.compile(r'\b[01]+[Bb]\b |\b[0-7]+[Oo]\b|\b[0-9A-Fa-f]+[Hh]\b|\b\d+[Dd]?\b|\b\d+(\.\d+)?[Ee][+-]?\d+\b|\b\d*\.\d+\b', re.VERBOSE)

    def __init__(self, data: str):
        self.src = data
        self.out_dir = f"{get_global_config().OUT_DIR}/lex"

    def analyze(self):
        self.analyze_numbers()
        print(self.src)
        self.analyze_key_words()
        print(self.src)
        self.analyze_delimeters()
        print(self.src)
        self.analyze_identifiers()
        print(self.src)

    def analyze_key_words(self):
        os.makedirs(f"{self.out_dir}",exist_ok=True)
        keywords_handler = KeyWordsParser()
        parsed = keywords_handler.parse(self.src)
        self.src = parsed['data']
        with open(f"{self.out_dir}/tw.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(parsed['matches']))

    def analyze_delimeters(self):
        os.makedirs(f"{self.out_dir}", exist_ok=True)
        parsed = DelimitersParser().parse(self.src)
        self.src = parsed['data']
        with open(f"{self.out_dir}/tl.txt", "w", encoding='utf-8') as f:
            f.write('\n'.join(parsed['matches']))

    def analyze_numbers(self):
        os.makedirs(f"{self.out_dir}", exist_ok=True)
        parsed = NumbersParser().parse(self.src)
        self.src = parsed['data']
        with open(f"{self.out_dir}/tn.txt", "w", encoding='utf-8') as f:
            f.write('\n'.join(parsed['matches']))

    def analyze_identifiers(self):
        os.makedirs(self.out_dir, exist_ok=True)
        parsed = IdentifiersParser().parse(self.src)
        self.src = parsed['data']
        with open(f"{self.out_dir}/ti.txt", "w", encoding='utf-8') as f:
            f.write("\n".join(parsed['matches']))


class LexemesParser(ABC):
    @abstractmethod
    def get_table_path(self):
        pass

    def __init__(self):
        path = self.get_table_path()
        f = open(path, "r", encoding='utf-8')
        items = []
        for line in f:
            l = line.strip()
            items.append(l)
        #self.pattern = r'\b(' + r"|".join(items) + r')\b'
        #self.pattern = r'(' + r"|".join(items) + r')'
        self.pattern = "|".join(items)
        self.pattern = re.compile(self.pattern, re.VERBOSE)

    def parse(self, data: str)->dict:
        matches = self.pattern.findall(data)
        return {"matches": matches, "data": re.sub(self.pattern, "", data)}


class KeyWordsParser(LexemesParser):
    def get_table_path(self):
        path = f"{get_global_config().RES_DIR}/tw.txt"
        return path

class DelimitersParser(LexemesParser):
    def get_table_path(self):
        return f"{get_global_config().RES_DIR}/tl.txt"
class NumbersParser(LexemesParser):
    def get_table_path(self):
        return f"{get_global_config().RES_DIR}/tn.txt"
class IdentifiersParser(LexemesParser):
    def get_table_path(self):
        return f"{get_global_config().RES_DIR}/ti.txt"

