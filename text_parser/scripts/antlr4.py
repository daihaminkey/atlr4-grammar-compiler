import re
import os
from pathlib import Path
from typing import List, Optional

from text_parser.scripts.grammar import Grammar
from text_parser.utils import run


class Antlr4:
    jar_path: Path = None

    available_languages = (
        'Java',
        'Python2',
        'Python3',
        'JavaScript',
        'Go',
        'Swift',
        'CSharp',
        'Cpp',
    )

    @staticmethod
    def classpath() -> str:
        return '-classpath {}'.format(Antlr4.jar_path)

    @staticmethod
    def compile_grammar(grammar: Grammar, language: str, output_path: Path) -> None:
        restore_path = Antlr4.handle_lang_insertions(grammar, language)

        run(
            f'java {Antlr4.classpath()} org.antlr.v4.Tool {grammar.path.absolute()} -Dlanguage={language} -o {output_path.absolute()}')
        print(f'Парсер {language} для грамматики {grammar.name} скомпилирован')

        if restore_path:
            os.remove(str(grammar.path.absolute()))
            restore_path.rename(grammar.path.absolute())

    # TODO слишком большой метод, разбить на маленькие
    @staticmethod
    def handle_lang_insertions(grammar: Grammar, language: str) -> Optional[Path]:
        grammar_dir: Path = grammar.path.parent
        lang_insertion_dir = grammar_dir / 'lang_insertions' / language

        if not lang_insertion_dir.exists():
            return

        insertion_patter = re.compile(r'-->\s?(\w+)\s?<--')

        with grammar.path.open('r') as grammar_file:
            file_content = grammar_file.read()
        matches: List[str] = insertion_patter.findall(file_content)

        if not matches:
            return

        tmp_grammar_path: Path = (grammar_dir / f'{grammar.name[:-3]}_tmp.g4').absolute()
        print(f'Сохраняю грамматику без вставок в файл {tmp_grammar_path}')
        grammar.path.absolute().rename(tmp_grammar_path)

        for match in matches:
            print(f'Произвожу замену языко-специфичного встраивания: {match}')
            match_pattern = re.compile(r'-->\s?' + match+ r'\s?<--')
            with (lang_insertion_dir / f'{match}.txt').open('r') as insertion_file:
                data_to_replace = insertion_file.read()
                data_to_replace = data_to_replace.replace('\\', '\\\\')

            file_content = match_pattern.sub(data_to_replace, file_content)

        print(f'Сохраняю грамматику со вставками в файл {grammar.path.absolute()}')

        grammar.path.absolute().write_text(file_content, encoding='utf-8')

        return tmp_grammar_path


