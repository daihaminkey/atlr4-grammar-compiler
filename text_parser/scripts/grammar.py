from pathlib import Path

from atlr4_compiler.compile_options import GrammarConfig
from text_parser.utils import calculate_hash


class Grammar:
    def __init__(self, config: GrammarConfig):
        if str(config.grammar_file)[-3:] != '.g4':
            raise NameError(config.grammar_file)

        self.path = config.grammar_file
        self.name = config.grammar_file.name
        self.hash = calculate_hash(self.path)

        self.root_rule = config.root_grammar_rule
