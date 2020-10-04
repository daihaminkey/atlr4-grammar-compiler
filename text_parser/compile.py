import argparse
import os
import shutil
from collections import namedtuple
from pathlib import Path
from typing import Dict

from atlr4_compiler.compile_options import GrammarConfig, CompilationConfig, PathConfig
from text_parser.scripts.antlr4 import Antlr4
from text_parser.scripts.grammar import Grammar
from text_parser.scripts.parser import Parser
from text_parser.scripts.test_rig import TestRig
from text_parser.utils import run


ConfigFromArgs = namedtuple(
    'ConfigFromArgs',
    'grammar_config, compilation_config, path_config'
)


def get_commandline_args() -> ConfigFromArgs:
    parser = argparse.ArgumentParser(description='Скрипт, компилирующий грамматику в парсер')

    parser.add_argument('-g', '-grammar', type=str, default='InputGrammar', dest='grammar', metavar='grammar',
                        help='Имя грамматики [ InputGrammar ] ')

    parser.add_argument('-l', '-lang', type=str, default=['Python3'], dest='lang', metavar='lang', nargs='+',
                        choices=Antlr4.available_languages,
                        help=f'Языки для компиляции [ Python3 ]')

    parser.add_argument('-r', '-root', type=str, default='root', dest='root', metavar='root',
                        help='Правило, с которого будет начинаться разбор [ root ] ')

    parser.add_argument('-j', '-jar', type=str, default='../antlr-4.7.2-complete.jar', dest='jar', metavar='jar',
                        help='Путь до скомпилированной библиотеки antlr4. К проекту прилагается по адресу [ ../antlr-4.7.2-complete.jar ]')

    parser.add_argument('-o', '-output', type=str, default='./generated_parsers', dest='output', metavar='output',
                        help='Задает каталог, в котором будут созданы классы listerner`ов [ generated_parsers ]')

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

    return ConfigFromArgs(
        GrammarConfig(
            grammar_file=Path('./grammar') / args.grammar,
            root_grammar_rule=args.root,
        ),
        CompilationConfig(
            lang_list=args.lang,
            is_recompile_forced=args.force,
            is_tests_forced=args.test,
            is_gui_test_needed=args.gui_test,
        ),
        PathConfig(
            jar_path=Path(args.jar),
            output_dir=Path(args.output),
            test_dir = Path('../tests')
        )
    )


def compile_grammar(
        grammar_config: GrammarConfig,
        compilation_config: CompilationConfig,
        path_config: PathConfig) -> None:

    Antlr4.jar_path = path_config.jar_path

    grammar = Grammar(grammar_config)
    parsers: Dict[str, Parser] = dict()

    for lang in Antlr4.available_languages:
        lang_dir = path_config.output_dir / lang
        if lang in compilation_config.lang_list:
            parsers[lang] = Parser(grammar, lang, lang_dir, compilation_config.is_recompile_forced)
        elif os.path.exists(lang_dir):
            print(f'Удаление директории {lang_dir}')
            shutil.rmtree(lang_dir)

    if compilation_config.is_gui_test_needed:
        TestRig(parsers['Java']).run_test_rig(Path('../tests/samples/test_sample.txt'))  # FIXME hardcode is bad

    if 'Python3' in parsers and (parsers['Python3'].is_recompiled or compilation_config.is_tests_forced):
        print('\n\nЗапускаю тесты грамматики...\n\n')

        run(f'pytest {path_config.test_dir}', timeout=60)


def compile_grammar_from_cli() -> None:
    compile_grammar(*get_commandline_args())


if __name__ == '__main__':
    compile_grammar_from_cli()
