
// Example grammar, supports bunch of lines from ['a', 'A', 'b', 'B']

grammar InputGrammar;

root : file_input ;

file_input : (NEWLINE | language_block)* EOF;

language_block : A | B;

A : 'a' | 'A';
B : 'b' | 'B';
NEWLINE : '\r\n' | '\r' | '\n';