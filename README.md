# INTERLIS 2.4 Parser

This is a parser for the INTERLIS 2.4 language.

## Package installation

```bash
pip install antlr4-tools
```

## Usage

```bash
antlr4-parse InterlisLexer.g4 InterlisParser.g4 <rule> <inputfile.extension>
```

### Options

- `-tree`: Show the parse tree.
- `-gui`: Show the parse tree in a graphical interface.
- `-tokens`: Show the tokens.

You can also use parse an expression directly from the command line.

```bash
antlr4-parse InterlisLexer.g4 InterlisParser.g4 <startRule> -tree
<input_expression>
^D
```
## Generating the parser

```bash
antlr4 -Dlanguage=Python3 InterlisLexer.g4 InterlisParser.g4
```
## Current status

- [ ] Grammar definition: the grammar is currently being defined and tested.
- [ ] Parser implementation: the parser will be implemented after the grammar is defined.

## References

- [antlr4-tools](https://github.com/antlr/antlr4-tools)
