# INTERLIS 2.4 Parser

A parser for the INTERLIS 2.4 language.

## Package Installation

Run the `start.sh` script to create a virtual environment and install the required packages.

## Usage

To parse an input file, use the following command:

```bash
antlr4-parse InterlisLexer.g4 InterlisParser.g4 <rule> input/<inputfile.extension>
```

### Options

- `-tree`: Display the parse tree.
- `-gui`: Display the parse tree in a graphical interface.
- `-tokens`: Display the tokens.

You can also parse an expression directly from the command line:

```bash
antlr4-parse InterlisLexer.g4 InterlisParser.g4 <startRule> -tree
<input_expression>
^D
```

## Generating the Parser

Generate the parser with the following command:

```bash
antlr4 -Dlanguage=Python3 InterlisLexer.g4 InterlisParser.g4
```

## Optional

To deactivate and remove the virtual environment, run the `clean.sh` script.

## Current Status

- [ ] Grammar definition: Currently being defined and tested.
- [ ] Parser implementation: To be implemented after the grammar is defined.

## References

- [antlr4-tools](https://github.com/antlr/antlr4-tools)
