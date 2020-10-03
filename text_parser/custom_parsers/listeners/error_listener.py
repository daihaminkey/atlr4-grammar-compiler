from antlr4.Token import CommonToken
from antlr4.error.ErrorListener import ErrorListener


class GrammarSyntaxError(Exception):
    def __init__(self, token: CommonToken, msg: str, line: int, column: int):
        token_text = None if token is None else token.text
        super().__init__(f'invalid token \'{token_text}\' [{line}:{column}]\n\n{msg}')


class GrammarAmbiguityError(Exception):
    pass


class GrammarAttemptingFullContextError(Exception):
    pass


class GrammarContextSensitivityError(Exception):
    pass


# noinspection PyPep8Naming
class CustomErrorListener(ErrorListener):

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise GrammarSyntaxError(offendingSymbol, msg, line, column)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise GrammarAmbiguityError(dfa)

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise GrammarAttemptingFullContextError(dfa)

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise GrammarContextSensitivityError(dfa)
