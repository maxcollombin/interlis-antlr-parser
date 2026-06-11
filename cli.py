import sys
import argparse
from pathlib import Path
from urllib.parse import urlparse
from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from interlis_antlr_parser.grammar.generated.InterlisLexer import InterlisLexer
from interlis_antlr_parser.grammar.generated.InterlisParser import InterlisParser
from model.ili_visitor import IliVisitor
from model.resolver import IliResolver
from model.dump import dump
from model.xtf_validator import validate_xtf
from model.xtf_parser import XTFParser


class SyntaxErrorListener(ErrorListener):
    """Listener pour capturer les erreurs syntaxiques ANTLR."""
    def __init__(self):
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"Ligne {line}:{column} - {msg}")


def extract_repositories_from_xtf(xtf_file: str) -> list:
    """
    Extract model repository URIs from XTF file.
    
    Looks for namespace declarations in root element (xmlns:ModelName="http://...")
    and returns repository bases derived from those URIs.
    
    Args:
        xtf_file: Path to XTF file
        
    Returns:
        List of repository URLs extracted from namespace URIs
    """
    import re
    
    try:
        repositories = set()
        
        # Read the first few lines to find namespace declarations
        with open(xtf_file, 'r', encoding='utf-8') as f:
            # Read enough to capture all namespace declarations (usually in first ~2KB)
            content = f.read(10000)
        
        # Find all xmlns declarations with URLs
        # Pattern: xmlns:ModelName="http(s)://.../ModelName"
        pattern = r'xmlns:([A-Za-z_][A-Za-z0-9_]*?)=["\'](https?://[^"\']+)["\']'
        matches = re.findall(pattern, content)
        
        for prefix, uri in matches:
            if prefix in ('ili', 'geom', 'xsi'):
                continue
            # Derive repository base from namespace URI
            # Example: http://www.interlis.ch/xtf/2.4/DMAV_Bodenbedeckung_V1_0
            # -> http://www.interlis.ch/xtf/2.4/
            base = uri.rstrip('/')
            if '/' in base:
                base = base.rsplit('/', 1)[0] + '/'
            repositories.add(base)
        
        return sorted(list(repositories))
    except Exception:
        # If we can't parse the XTF, just return empty list
        return []


def check_syntax(ili_file, verbose=False):
    """Vérifie la syntaxe d'un fichier INTERLIS."""
    if verbose:
        print(f"Vérification de la syntaxe de {ili_file}...", file=sys.stderr)
    
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
        print(f"Erreurs syntaxiques détectées:", file=sys.stderr)
        for error in error_listener.errors:
            print(f"   {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Syntaxe OK", file=sys.stderr)
        sys.exit(0)


def main():
    """Pipeline : Lexing → Parsing → Visiting → Resolving → Serializing."""
    
    # Arguments avec argparse
    parser = argparse.ArgumentParser(
        description="Analyze an INTERLIS (.ili) model and return its structure"
    )
    parser.add_argument(
        "ili_file",
        nargs="?",
        default=None,
        help="INTERLIS model file to process (optional if --validate-xtf is used)"
    )
    parser.add_argument(
        "-c", "--check",
        action="store_true",
        help="Check syntax only, do not build the model"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show processing steps"
    )
    parser.add_argument(
        "--validate-xtf",
        metavar="XTF_FILE",
        help="Validate an XTF file against the INTERLIS model"
    )
    parser.add_argument(
        "--ili-model",
        help="Local path or URL of an ILI model to use for validation"
    )
    parser.add_argument(
        "--model-repo",
        action="append",
        help="URL or local directory of a model repository (semicolon-separated for multiple)."
    )
    parser.add_argument(
        "--log-file",
        help="Write validation result to a log file"
    )
    
    args = parser.parse_args()
    
    # Process model repositories (remote URLs or local directories)
    model_repos = []
    local_repos = []
    if args.model_repo:
        # Support semicolon-separated list in a single argument
        repo_args = []
        for repo_arg in args.model_repo:
            repo_args.extend([r.strip() for r in repo_arg.split(';') if r.strip()])
        for repo in repo_args:
            if repo.startswith('http://') or repo.startswith('https://'):
                model_repos.append(repo)
            else:
                # Treat as local directory
                local_repos.append(repo)
    
    # Mode validation XTF - can work without explicit model
    if args.validate_xtf:
        xtf_file = Path(args.validate_xtf)
        if not xtf_file.exists():
            print(f"Erreur: Fichier XTF {xtf_file} introuvable.", file=sys.stderr)
            sys.exit(1)

        def is_url(value: str) -> bool:
            parsed = urlparse(value)
            return parsed.scheme in ("http", "https")
        
        ili_file = None
        if args.ili_model:
            ili_file = args.ili_model
            if not is_url(ili_file):
                ili_path = Path(ili_file)
                if not ili_path.exists():
                    print(f"Erreur: Fichier ILI {ili_path} introuvable.", file=sys.stderr)
                    sys.exit(1)
        elif args.ili_file:
            ili_path = Path(args.ili_file)
            if not ili_path.exists():
                print(f"Erreur: Fichier ILI {ili_path} introuvable.", file=sys.stderr)
                sys.exit(1)
            ili_file = str(ili_path)
        
        log_lines = []

        def emit(line="", stream=sys.stdout, always_log=True):
            # Always log to log_lines if log_file is set
            if args.log_file:
                log_lines.append(line)
            # Always print to terminal if verbose or if error (stderr)
            if args.verbose or stream != sys.stdout:
                print(line, file=stream)

        # Auto-discover repositories from XTF if not explicitly provided
        if not model_repos and not local_repos:
            discovered_repos = extract_repositories_from_xtf(str(xtf_file))
            if discovered_repos and args.verbose:
                emit(f"Discovered repositories in XTF header: {discovered_repos}", stream=sys.stderr)
            model_repos.extend(discovered_repos)

        # Always emit validation step messages in English
        if args.verbose:
            if ili_file:
                emit(f"Validating {xtf_file} against {ili_file}...", stream=sys.stderr)
            else:
                if model_repos:
                    def repo_root(url):
                        import urllib.parse
                        parsed = urllib.parse.urlparse(url)
                        return f"{parsed.scheme}://{parsed.netloc}" if parsed.scheme and parsed.netloc else url.rstrip('/')
                    unique_roots = set(repo_root(r) for r in model_repos)
                    emit(f"Validating {xtf_file} with {len(unique_roots)} repository(ies)...", stream=sys.stderr)
                else:
                    emit(f"Validating {xtf_file} with model auto-discovery (no repository specified)...", stream=sys.stderr)

        # (Debug output removed for normal operation)
        
        result = validate_xtf(
            str(xtf_file),
            str(ili_file) if ili_file else None,
            model_repositories=model_repos,
            local_repositories=local_repos if local_repos else None,
        )
        
        # Simple validation message
        if result.is_valid:
            emit("Validation passed")
        else:
            emit("Validation failed")
        
        # Show errors if any
        if result.errors:
            emit("\nERRORS:")
            for error in result.errors:
                emit(f"  {error}")
        
        # Show warnings if any
        if result.warnings:
            emit("\nWARNINGS:")
            for warning in result.warnings:
                emit(f"  {warning}")
        
        # Show info if verbose
        if result.info and args.verbose:
            emit("\nINFO:")
            for info in result.info:
                emit(f"  {info}")
        
        # If no models loaded and no repository provided, give helpful message
        if not model_repos and not ili_file and result.warnings:
            emit("\nHINT: To validate XTF files, provide one of:", stream=sys.stderr)
            emit("  1. A model file:      python cli.py model.ili --validate-xtf data.xtf", stream=sys.stderr)
            emit("  2. A model repository: python cli.py --validate-xtf data.xtf --model-repo https://models.interlis.ch", stream=sys.stderr)
            emit("  3. Repository URIs will be auto-discovered from XTF header if present", stream=sys.stderr)

        if args.log_file:
            try:
                Path(args.log_file).write_text("\n".join(log_lines) + "\n", encoding="utf-8")
            except Exception as e:
                print(f"Erreur: impossible d'écrire le fichier log {args.log_file}: {e}", file=sys.stderr)
        
        sys.exit(0 if result.is_valid else 1)
    
    # For other modes, require ili_file
    if not args.ili_file:
        print("Erreur: Fichier INTERLIS requis (sauf en mode --validate-xtf).", file=sys.stderr)
        parser.print_help(file=sys.stderr)
        sys.exit(1)
    
    ili_file = Path(args.ili_file)
    
    # Si --check, vérifier la syntaxe uniquement
    if args.check:
        check_syntax(ili_file, verbose=args.verbose)
        return
    
    # Phase 1 : Lexing & Parsing
    if args.verbose:
        print(f"Lexing & Parsing {ili_file}...", file=sys.stderr)
    input_stream = FileStream(str(ili_file), encoding='utf-8')
    lexer = InterlisLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = InterlisParser(stream)
    tree = parser.interlis2def()
    
    # Phase 2 : Visiting (construction AST)
    if args.verbose:
        print("Constructing AST...", file=sys.stderr)
    visitor = IliVisitor(debug=args.verbose)
    model = visitor.visit(tree)
    
    if not model:
        print(" Erreur: Aucun modèle construit.", file=sys.stderr)
        sys.exit(1)
    
    if args.verbose:
        print(f"Modèle '{model.name}' construit ({len(model.topics)} topics)", file=sys.stderr)
    
    # Phase 3 : Resolving (résolution sémantique)
    if args.verbose:
        print("Resolving semantic references...", file=sys.stderr)
    resolver = IliResolver(model)
    model = resolver.resolve()
    
    if args.verbose:
        print(f"Modèle résolu ({len(model._classes_index)} classes indexées)", file=sys.stderr)
    
    # Phase 4 : Serializing
    if args.verbose:
        print(f"Serializing to DUMP...", file=sys.stderr)
    
    output = dump(model)
    print(output)


if __name__ == "__main__":
    main()
