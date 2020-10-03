from pathlib import Path

from text_parser.custom_parsers import InputGrammarListener, InputGrammarParser


class RootListener(InputGrammarListener):
    def __init__(self, file_path: Path):
        pass

    def enterRoot(self, ctx: InputGrammarParser.RootContext):
        pass

    def exitRoot(self, ctx: InputGrammarParser.RootContext):
        pass
