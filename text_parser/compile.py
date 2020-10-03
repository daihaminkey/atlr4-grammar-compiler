import argparse
import os
import shutil
from collections import namedtuple
from pathlib import Path
from typing import Dict

from text_parser.scripts.antlr4 import Antlr4
from text_parser.scripts.grammar import Grammar
from text_parser.scripts.parser import Parser
from text_parser.scripts.test_rig import TestRig
from text_parser.utils import run

Args = namedtuple(
    'Args',
    'grammar_file_name, root_grammar_rule, lang_list, force_recompile, force_test, gui_test_needed'
)


def get_dev_args() -> Args:
    return Args(
        grammar_file_name='InputGrammar.g4',
        root_grammar_rule='root',
        lang_list='Python3',
        force_recompile=False,
        force_test=True,
        gui_test_needed=False,
    )


def get_commandline_args() -> Args:
    parser = argparse.ArgumentParser(description='Скрипт, компилирующий грамматику в парсер')

    parser.add_argument('-g', '-grammar', type=str, default='InputGrammar', dest='grammar', metavar='grammar',
                        help='Имя грамматики [ InputGrammar ] ')

    parser.add_argument('-l', '-lang', type=str, default=['Python3'], dest='lang', metavar='lang', nargs='+',
                        choices=Antlr4.available_languages,
                        help=f'Языки для компиляции [ Python3 ]')

    parser.add_argument('-r', '-root', type=str, default='root', dest='root', metavar='root',
                        help='Правило, с которого будет начинаться разбор [ root ] ')

    parser.add_argument('-f', '-force', action='store_true', default=False, dest='force',
                        help='Принудительно рекомпилировать грамматику')

    parser.add_argument('-t', '-test', action='store_true', default=False, dest='test',
                        help='Принудительно запустить тесты')

    parser.add_argument('-gui', '-gui_test', action='store_true', default=False, dest='gui_test',
                        help='Вывести GUI с деревом разбора (добавит Java к языкам для компиляции), требует JDK')

    # TODO [-gui|gui_test] path   | run test rig not on the hardcoded file

    args = parser.parse_args()

    if args.grammar[-3:] != '.g4':
        args.grammar += '.g4'

    if args.gui_test and 'Java' not in args.lang:
        args.lang.append('Java')

    return Args(args.grammar, args.root, args.lang, args.force, args.test, args.gui_test)


def compile_grammar(args: Args, jar_path: Path, grammar_dir: Path, output_dir: Path, test_dir: Path) -> None:
    Antlr4.jar_path = jar_path

    grammar_path = grammar_dir / args.grammar_file_name

    grammar = Grammar(grammar_path, args.root_grammar_rule)
    parsers: Dict[str, Parser] = dict()

    for lang in Antlr4.available_languages:
        lang_dir = output_dir / lang
        if lang in args.lang_list:
            parsers[lang] = Parser(grammar, lang, lang_dir, args.force_recompile)
        elif os.path.exists(lang_dir):
            print(f'Удаление директории {lang_dir}')
            shutil.rmtree(lang_dir)

    if args.gui_test_needed:
        TestRig(parsers['Java']).run_test_rig(Path('../tests/samples/test_sample.txt'))  # FIXME хардкод такой хардкод

    if 'Python3' in parsers and (parsers['Python3'].is_recompiled or args.force_test):
        print('\n\nЗапускаю тесты грамматики...\n\n')

        run(f'pytest {test_dir}', timeout=60)


def compile_domain_specific_grammar(args: Args) -> None:
    compile_grammar(args=args,
                    jar_path=Path('./scripts/antlr-4.7.2-complete.jar'),
                    grammar_dir=Path('./grammar'),
                    output_dir=Path('./generated_parsers'),
                    test_dir=Path('../tests')
                    )


if __name__ == '__main__':
    compile_domain_specific_grammar(args=get_commandline_args())
