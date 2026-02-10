# interlis-antlr-parser

A comprehensive Python toolkit for converting INTERLIS 2.4 models to multiple formats:

**Core Features:**

- Parse INTERLIS models (.ili) using ANTLR4
- Convert to Python dataclasses with Pydantic validation
- Export to JSON Schema for API/validation
- Generate CartoSym CSS & JSON for cartographic styling
- XTF transfer file validation

## Installation

### Quick Start

```sh
git clone https://github.com/maxcollombin/interlis-antlr-parser.git
cd interlis-antlr-parser

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the package
pip install -e .
```

### Development Setup (with grammar modification support)

If you need to regenerate the ANTLR parser from grammar files:

```sh
pip install -e ".[dev]"
```

To regenerate the parser after modifying grammar files:

```sh
cd grammar  # Go to the submodule
./regenerate.sh  # Or run antlr4 commands directly
```

## CLI Usage

After installation, use `python` from the activated virtual environment:

```sh
python -m cli -h                              # Show help
python -m cli [file.ili]                      # Parse and display the model
python -m cli [file.ili] > output.dump        # Export to file
python -m cli [file.ili] --check              # Check syntax only
python -m cli [file.ili] --check --verbose    # Syntax check with details
```

## Cleanup

To clean up the workspace:

```sh
# Remove all files ignored by .gitignore
git clean -fdx

# Or selectively uninstall and purge pip cache
pip uninstall -y interlis-antlr-parser
pip cache purge
```

## Architecture

The toolkit converts INTERLIS models through multiple representations:

- **ANTLR4**: Grammar-based parsing of INTERLIS 2.4 syntax
- **Pydantic v2**: Type-safe Python model definitions with validation
- **Visitor Pattern**: AST traversal and semantic model instantiation
- **Multiple Export Formats**: Python, JSON Schema, CartoSym CSS/JSON

### Project Structure

```txt
model/
  ├── core.py          # Model, Class, Topic, Package, MetaElement
  ├── types.py         # Type system (TextType, NumericType, EnumType)
  ├── attributes.py    # Attribute, MetaAttribute, Role
  ├── constraints.py   # Constraint types
  ├── expressions.py   # Expression types
  ├── domain.py        # Domain types
  ├── functions.py     # Function definitions
  ├── multiplicity.py  # Multiplicity definitions
  └── parser.py        # ANTLR Visitor implementation

cli.py               # CLI entry point
converter.py         # Conversion utilities
```
