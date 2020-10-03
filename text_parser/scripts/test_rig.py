from pathlib import Path

from text_parser.scripts.antlr4 import Antlr4
from text_parser.scripts.parser import Parser
from text_parser.utils import run


class TestRig:

    def __init__(self, parser: Parser):
        if parser.language != 'Java':
            raise AttributeError

        self.parser = parser

    @property
    def classpath(self) -> str:
        classpath_lines = (
            str(Antlr4.jar_path),
            str(self.parser.dir)
        )
        return '-classpath {}'.format(';'.join(classpath_lines))

    def run_test_rig(self, input_path: Path) -> None:
        if self.parser.is_recompiled:
            self.compile_java_parser()
        self.start_test_rig(input_path)

    def start_test_rig(self, input_path: Path) -> None:
        print('Запуск интерфейса визуализации разбора...')
        with input_path.open() as input_file:
            run(
                f'java {self.classpath} org.antlr.v4.gui.TestRig {self.parser.grammar.name} {self.parser.grammar.root_rule} -encoding=utf-8 -gui',
                stdin=input_file,
                timeout=None)

    def compile_java_parser(self) -> None:
        print('Компиляция Java-классов...')
        java_files_mask = self.parser.dir / '*.java'
        run(f'javac {Antlr4.classpath()} {java_files_mask.absolute()}', timeout=15)
