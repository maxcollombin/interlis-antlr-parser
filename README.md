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
python -m cli [file.ili] --validate-xtf [file.xtf]  # Validate XTF transfer file
python -m cli [file.ili] --validate-xtf [file.xtf] -v  # Verbose validation
python -m cli [file.ili] --validate-xtf [file.xtf] --log-file validation.log  # Write validation output to a log file
```

### XTF Validation

Validate INTERLIS transfer files (.xtf) against their model definitions:

```sh
# Basic validation with explicit model
python -m cli input/myModel.ili --validate-xtf input/myModel.xtf

# Verbose validation with detailed output
python -m cli input/myModel.ili --validate-xtf input/myModel.xtf -v

# Auto-discover models from XTF (no explicit model required)
python -m cli --validate-xtf input/myData.xtf -v

# Validate with remote model repositories (streaming, no disk caching)
python -m cli --validate-xtf input/myData.xtf --model-repo https://models.example.com -v

# Write validation output to a log file
python -m cli --validate-xtf input/myData.xtf --log-file validation.log

# Validate with an explicit local or remote ILI model
python -m cli --validate-xtf input/myData.xtf --ili-model input/MyModel.ili
python -m cli --validate-xtf input/myData.xtf --ili-model https://models.example.com/MyModel.ili
```

#### How XTF Validation Works

The XTF validator supports two modes:

**Mode 1: Explicit Model Validation**
```sh
python -m cli input/MyModel.ili --validate-xtf input/MyModel.xtf
```
When you provide an explicit model file, the validator checks the XTF data against that specific model.

**Mode 2: Auto-Discovery from XTF (New)**
```sh
python -m cli --validate-xtf input/MyData.xtf -v
```
When no explicit model is provided, the validator:
1. Reads the XTF header for model references
2. Extracts model names from XML namespace prefixes (e.g., `DMAV_Dienstbarkeitsgrenzen_V1_0` → model name)
3. Attempts to load models from:
   - Local directory (same location as XTF file)
   - Remote repositories (if specified via `--model-repo`)

#### Model Namespace Extraction

The validator automatically identifies models from XML namespaces in the XTF structure:

```xml
<!-- Example XTF structure -->
<DMAV_Dienstbarkeitsgrenzen_V1_0:Dienstbarkeitsgrenzen ili:bid="...">
  <!-- DMAV_Dienstbarkeitsgrenzen_V1_0 = model name -->
  <!-- Dienstbarkeitsgrenzen = topic name -->
</DMAV_Dienstbarkeitsgrenzen_V1_0:Dienstbarkeitsgrenzen>
```

#### Model Resolution Strategy

When auto-discovering models, the validator tries these approaches in order:

1. **Local Model Files**: Looks for `ModelName.ili` in the same directory as the XTF file
2. **Remote Repositories (Streaming)**: Queries repository metadata index (`ilimodels.xml`) to find models, then streams them directly without caching to disk
3. **Fallback Repository Resolution**: Uses repositories specified via `--model-repo` flag

#### Remote Model Repositories with Streaming

Configure remote model repositories for streaming model loading (no disk caching):

```sh
# Single repository
python -m cli --validate-xtf input/data.xtf --model-repo https://models.example.com -v

# Multiple repositories
python -m cli --validate-xtf input/data.xtf \
  --model-repo https://models.example.com \
  --model-repo https://models2.example.com -v
```

**How streaming works:**
1. Validator queries `ilimodels.xml` at repository root to discover available models
2. For each required model, streams content directly from HTTP (no local disk storage)
3. Models are parsed in-memory and indexed for validation
4. Session-level memory cache avoids re-downloading the same model multiple times
5. No `.interlis_cache/` directory created

##### Supported Repository Formats

Repositories must contain the following structure:
```
https://models.example.com/
├── ilimodels.xml      (required - metadata index of available models)
├── ilisite.xml        (required - site metadata)
├── ilidata.xml        (optional - object catalog)
├── ModelName1.ili     (model files)
├── ModelName2.ili
└── ...
```

The `ilimodels.xml` format:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<RepositoryIndex>
  <Models>
    <Model>
      <Name>ModelName</Name>
      <Version>1.0</Version>
      <File>path/to/ModelName.ili</File>
    </Model>
  </Models>
</RepositoryIndex>
```

#### Example: Local and Multiple Repository Integration

For Swiss data from a local directory:

```sh
python -m cli --validate-xtf input/DMAVTYM_Alles_V1_0.xtf \
  --model-repo input/ -v
```

For Swiss data with multiple repositories (semicolon-separated):

```sh
python -m cli --validate-xtf input/DMAVTYM_Alles_V1_0.xtf \
  --model-repo "input/;https://models.geo.admin.ch/V_D/;https://models.interlis.ch/refhb24/" -v
```

You can mix local directories and remote URLs. The validator will check each repository in order.

---

The CLI supports the `-h` or `--help` flag for usage information:

```sh
python -m cli -h
```

#### Validation Output

The validator reports:

- **Errors**: Data incompatible with model (fails validation)
  - Missing required models
  - Unknown classes or topics
  - Invalid attribute types
  - Missing mandatory attributes
  - Broken object references

- **Warnings**: Issues that don't fail validation
  - Models loaded from alternate sources
  - Catalog files detected
  - Missing optional files

- **Info** (verbose mode `-v`):
  - Model discovery progress
  - Number of models loaded
  - Streaming source information
  - Repository metadata details
  - Catalog file details

#### Example: Remote Repository Integration

For Swiss data from a remote repository:

```sh
python -m cli --validate-xtf input/DMAVTYM_Alles_V1_0.xtf \
  --model-repo https://models.geo.admin.ch/V_D/ -v
```

The validator checks:
- Model references in XTF header
- Object class definitions across all referenced models
- Attribute types and constraints
- Mandatory attributes presence
- Reference integrity between objects
- Cross-model references

#### Performance Notes

- **Streaming mode**: No disk I/O overhead, models kept in memory during validation session
- **Session caching**: Models downloaded once per validation session, then cached in memory
- **Bandwidth-efficient**: Only downloads metadata and required models
- **Multi-repo support**: Can query multiple repositories simultaneously

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
  ├── transfer.py      # Transfer format models (XTF, XML)
  ├── xtf_parser.py    # XTF file parser
  ├── xtf_validator.py # XTF validation engine
  └── parser.py        # ANTLR Visitor implementation

cli.py               # CLI entry point
converter.py         # Conversion utilities
