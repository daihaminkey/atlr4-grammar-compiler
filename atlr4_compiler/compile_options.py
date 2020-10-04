from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class GrammarConfig:
    grammar_file: Path = Path('./grammar') / 'InputGrammar.g4'
    root_grammar_rule: str = 'root'


@dataclass
class CompilationConfig:
    lang_list: List[str] = ('Python3',)
    is_recompile_forced: bool = False,
    is_tests_forced: bool = False
    is_gui_test_needed: bool = False,


@dataclass
class PathConfig:
    jar_path: Path = Path('../antlr-4.7.2-complete.jar')
    output_dir: Path = Path('./generated_parsers')
    test_dir: Path = Path('../tests')
