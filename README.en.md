# ANTLR4 Grammar compiler

## What does the script do?

The `compile.py` script compiles grammars into a parser and, optionally, launches the TestRig.

The Java Parser is used to run `input.txt` content review visualization. // TODO: Update

The Parser on Python is used in further development.

## Before the launch

To work, you need to have `antlr-4.7.2-complete.jar` in the `text_parser/scripts/` folder, which is already included in the repository.

The JRE all that's required to work with Python, but Java compilations, including TestRig rendering, require the JDK.

## Using a script

The scripts run in the root of the repository:

```
$ cd project_path
$ py compile.py -h

usage: compile.py [-h] [-g grammar] [-l lang [lang ...]] [-r root] [-f] [-t] [-gui]

A script that compiles grammar into a parser

optional arguments:
  -h, --help            show this help message and exit
  -g grammar, -grammar grammar
                        Grammar Name [ InputGrammer ]
  -l lang [lang ...], -lang lang [lang ...]
                        Languages for compilation [ Python3 ]
  -r root, -root root   Path from which the analysis will begin [ root ]
  -f,-force             Force trecomopilation of the grammar
  -t,-test              Force running of the tests
  -gui, -gui_test       Deduce GUI with a parsing tree (adds Java to languages
                        for compilation), requires JDK
```

## Project Directory

`/custom_parser` - logic over generated parcels. You can inherit.

`/generated_parsers` - 'read only' compilation results antlr4, parsers in different languages

`/grammar` - antlr4-grammar

`/scripts` - Python scripts not used in prasing, but serving compilation

## Hashing

When the parser is generated, next to it a file `hash.md5` is created, in which the hash of the grammar parser is stored.
If the `-f` flag is not specified, only those parsers whose hashes are different will be re-recorded when compiling.

This will allow you to run tests in the future only when the original grammar changes, as well as monitor the relevance of the parser.

## .interp and .tokens

The script removes the intermediate files of q.interp and z.tokens generated in `/generated_parsers/LANG/`, since they aren't needed.
If they are suddenly needed, which is unlikely, you can modify `/scripts/parser.py`
