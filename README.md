# INTERLIS 2.4 Parser

A parser for the INTERLIS 2.4 language.

## Package Installation

Run `. start.sh` (or `source ./start.sh`) script to create a virtual environment and install the required packages.

## Usage

To parse an input file, use the following command:

```bash
antlr4-parse grammars/InterlisLexer.g4 grammars/InterlisParser.g4 <rule> input/<inputfile.extension> -<option>
```

### Options

- `-tree`: Display the parse tree.
- `-gui`: Display the parse tree in a graphical interface.
- `-tokens`: Display the tokens.

You can also parse an expression directly from the command line:

```bash
antlr4-parse grammars/InterlisLexer.g4 grammars/InterlisParser.g4 <startRule> -tree
<input_expression>
^D
```

## Generating the Parser

Generate the parser with the following command:

```bash
antlr4 -Dlanguage=Python3 grammars/InterlisLexer.g4 grammars/InterlisParser.g4
```

## Optional

To deactivate and remove the virtual environment, run `. clean.sh` script.

## Current Status

- [ ] Grammar definition: Currently being defined and tested.
    - [x] Handle the placeholders
    - [x] Refactor the lexer and parser files to have 2 clean and distinct ressources
    - [ ] Check for grammar consistency and corrections
    - [ ] Update the file Notes.md with the grammar inconsistencies
- [ ] Parser implementation: To be implemented after the grammar is defined.

## References

- [eCH-0031 INTERLIS 2 – Manuel de référence](https://ech.ch/sites/default/files/imce/eCH-Dossier/eCH-Dossier_PDF_Publikationen/Hauptdokument/STAN_f_DEF_2024-04-24_eCH-0031_V2.1.0_INTERLIS_2-Manuel_de_re%CC%81fe%CC%81rence.pdf)
- [antlr4-tools](https://github.com/antlr/antlr4-tools)
