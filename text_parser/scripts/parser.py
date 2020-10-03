from pathlib import Path

from text_parser.scripts.antlr4 import Antlr4
from text_parser.scripts.grammar import Grammar
from text_parser.utils import clear_dir, delete_files_by_patterns


class Parser:
    hash_file_name = 'hash.md5'

    @property
    def hash_path(self) -> Path:
        return self.dir / self.hash_file_name

    def __init__(self, grammar: Grammar, language: str, output_dir: Path, forced_recompile: bool = False):
        self.language = language
        self.dir = output_dir
        self.grammar = grammar
        self.is_recompiled = self.is_hash_not_matches() or forced_recompile

        if self.is_recompiled:
            self.compile()
        else:
            print(f'Парсер {self.language} уже соответствует грамматике {grammar.name}')

    def is_hash_not_matches(self) -> bool:
        if not self.hash_path.exists():
            return True

        with self.hash_path.open('r') as hash_file:
            return self.grammar.hash != hash_file.read()

    def compile(self):
        clear_dir(self.dir)
        Antlr4.compile_grammar(self.grammar, self.language, self.dir)
        delete_files_by_patterns(self.dir, '*.interp', '*.tokens')
        self.save_hash()

    def save_hash(self):
        with self.hash_path.open('w') as hash_file:
            hash_file.write(self.grammar.hash)
