import sys
import argparse
from pathlib import Path
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from interlis_antlr_parser.grammar.generated.InterlisLexer import InterlisLexer
from interlis_antlr_parser.grammar.generated.InterlisParser import InterlisParser
from model.ili_visitor import IliVisitor
from model.resolver import IliResolver
from model.dump import dump


class SyntaxErrorListener(ErrorListener):
    """Listener pour capturer les erreurs syntaxiques ANTLR."""
    def __init__(self):
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Ligne {line}:{column} - {msg}")


def check_syntax(ili_file, verbose=False):
    """Vérifie la syntaxe d'un fichier INTERLIS."""
    if verbose:
        print(f"🔍 Vérification de la syntaxe de {ili_file}...", file=sys.stderr)
    
    input_stream = FileStream(str(ili_file), encoding='utf-8')
    lexer = InterlisLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = InterlisParser(stream)
    
    # Remplacer les error listeners par défaut
    parser.removeErrorListeners()
    error_listener = SyntaxErrorListener()
    parser.addErrorListener(error_listener)
    
    # Parser le fichier
    parser.interlis2def()
    
    if error_listener.errors:
        print(f"❌ Erreurs syntaxiques détectées:", file=sys.stderr)
        for error in error_listener.errors:
            print(f"   {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"✅ Syntaxe OK", file=sys.stderr)
        sys.exit(0)


def main():
    """Pipeline : Lexing → Parsing → Visiting → Resolving → Serializing."""
    
    # Arguments avec argparse
    parser = argparse.ArgumentParser(
        description="Analyse un modèle INTERLIS (.ili) et retourne sa structure"
    )
    parser.add_argument(
        "ili_file",
        nargs="?",
        default="input/IlisMeta16.ili",
        help="Fichier INTERLIS à traiter"
    )
    parser.add_argument(
        "-c", "--check",
        action="store_true",
        help="Vérifier la syntaxe sans construire le modèle"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Afficher les étapes du traitement"
    )
    
    args = parser.parse_args()
    ili_file = Path(args.ili_file)
    
    if not ili_file.exists():
        print(f" Erreur: Fichier {ili_file} introuvable.", file=sys.stderr)
        sys.exit(1)
    
    # Si --check, vérifier la syntaxe uniquement
    if args.check:
        check_syntax(ili_file, verbose=args.verbose)
        return
    
    # Phase 1 : Lexing & Parsing
    if args.verbose:
        print(f"📖 Lexing & Parsing {ili_file}...", file=sys.stderr)
    input_stream = FileStream(str(ili_file), encoding='utf-8')
    lexer = InterlisLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = InterlisParser(stream)
    tree = parser.interlis2def()
    
    # Phase 2 : Visiting (construction AST)
    if args.verbose:
        print("🔨 Constructing AST...", file=sys.stderr)
    visitor = IliVisitor(debug=args.verbose)
    model = visitor.visit(tree)
    
    if not model:
        print(" Erreur: Aucun modèle construit.", file=sys.stderr)
        sys.exit(1)
    
    if args.verbose:
        print(f"✓ Modèle '{model.name}' construit ({len(model.topics)} topics)", file=sys.stderr)
    
    # Phase 3 : Resolving (résolution sémantique)
    if args.verbose:
        print(" Resolving semantic references...", file=sys.stderr)
    resolver = IliResolver(model)
    model = resolver.resolve()
    
    if args.verbose:
        print(f"✓ Modèle résolu ({len(model._classes_index)} classes indexées)", file=sys.stderr)
    
    # Phase 4 : Serializing
    if args.verbose:
        print(f" Serializing to DUMP...", file=sys.stderr)
    
    output = dump(model)
    print(output)


if __name__ == "__main__":
    main()
