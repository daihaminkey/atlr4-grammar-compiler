from pathlib import Path

from antlr4 import *

from text_parser.custom_parsers import InputGrammarParser, InputGrammarLexer
from text_parser.custom_parsers.listeners.error_listener import CustomErrorListener
from text_parser.generated_parsers.Python3 import InputGrammarListener


class Parse:

    @staticmethod
    def parse(path: Path, listener_cls, *args) -> InputGrammarListener:
        input_stream = FileStream(str(path), encoding='utf-8')

        listener = listener_cls(path, *args)
        error_listener = CustomErrorListener()

        lexer = InputGrammarLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)

        stream = CommonTokenStream(lexer)
        parser = InputGrammarParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        tree = parser.root()

        walker = ParseTreeWalker()
        walker.walk(listener, tree)
        return listener
