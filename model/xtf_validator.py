"""
XTF Validator - Validate INTERLIS Transfer Files against Models

This module validates INTERLIS Transfer Format (XTF) files against their
corresponding INTERLIS model definitions (.ili files).

Validation checks:
- Header validation (correct models referenced)
- Object validation (correct class names, attributes)
- Type validation (attribute values match type constraints)
- Cardinality validation (mandatory attributes present)
- Reference validation (references point to valid objects)

References: INTERLIS 2.4 Specification, XTF Format
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
import re
import urllib.request
import urllib.error
import urllib.parse

from .xtf_parser import XTFDocument, XTFObject, parse_xtf, XTFModelRef
from .remote_model_resolver import StreamingModelLoader, create_streaming_loader


@dataclass
class ValidationError:
    """
    A validation error found during XTF validation.
    
    Attributes:
        severity: Error severity (ERROR, WARNING, INFO)
        message: Human-readable error message
        object_tid: Transfer ID of the object (if applicable)
        attribute_name: Attribute name (if applicable)
        line_number: Line number in XTF file (if available)
    """
    severity: str  # ERROR, WARNING, INFO
    message: str
    object_tid: Optional[str] = None
    attribute_name: Optional[str] = None
    line_number: Optional[int] = None
    
    def __str__(self) -> str:
        parts = [f"[{self.severity}]", self.message]
        if self.object_tid:
            parts.append(f"(TID: {self.object_tid})")
        if self.attribute_name:
            parts.append(f"(Attribute: {self.attribute_name})")
        return " ".join(parts)


@dataclass
class ValidationResult:
    """
    Result of XTF validation.
    
    Attributes:
        is_valid: Whether the XTF file is valid
        errors: List of validation errors
        warnings: List of validation warnings
        info: List of informational messages
    """
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    info: List[ValidationError] = field(default_factory=list)
    
    def add_error(self, message: str, object_tid: Optional[str] = None, 
                  attribute_name: Optional[str] = None):
        """Add an error to the validation result."""
        self.errors.append(ValidationError(
            severity="ERROR",
            message=message,
            object_tid=object_tid,
            attribute_name=attribute_name
        ))
        self.is_valid = False
    
    def add_warning(self, message: str, object_tid: Optional[str] = None,
                    attribute_name: Optional[str] = None):
        """Add a warning to the validation result."""
        self.warnings.append(ValidationError(
            severity="WARNING",
            message=message,
            object_tid=object_tid,
            attribute_name=attribute_name
        ))
    
    def add_info(self, message: str):
        """Add informational message."""
        self.info.append(ValidationError(
            severity="INFO",
            message=message
        ))
    
    def summary(self) -> str:
        """Get a summary of validation results."""
        return (f"Validation {'PASSED' if self.is_valid else 'FAILED'}: "
                f"{len(self.errors)} errors, {len(self.warnings)} warnings")


class XTFValidator:
    """Validator for INTERLIS Transfer Format (XTF) files."""
    
    def __init__(self, model_path: Optional[str] = None, model_repositories: Optional[List[str]] = None, local_repositories: Optional[List[str]] = None):
        """
        Initialize the validator with an INTERLIS model.
        
        Args:
            model_path: Path to the .ili model file (optional - can be auto-discovered from XTF)
            model_repositories: Optional list of remote model repository base URLs
            local_repositories: Optional list of local model repository directories
        """
        self.model_path_raw = model_path
        self.model_path = None
        if model_path and not self._is_url(model_path):
            self.model_path = Path(model_path)
        self.model = None
        self.models: Dict[str, Any] = {}  # model_name -> model object
        self.classes_by_name: Dict[str, Any] = {}
        self.topics_by_name: Dict[str, Any] = {}
        self.model_repositories = model_repositories or []
        self.local_repositories = local_repositories or []
        self.local_models = {}
        self.catalog_items: Dict[str, Any] = {}  # TID -> catalog object
        self.namespace_to_model: Dict[str, str] = {}  # namespace prefix -> model name
        self.streaming_loader: Optional[StreamingModelLoader] = None
        if model_path:
            self._load_model()
        # Initialize streaming loader for remote repositories
        if self.model_repositories:
            self.streaming_loader = create_streaming_loader(self.model_repositories)
        # Support for local repositories
        if self.local_repositories:
            for repo_dir in self.local_repositories:
                repo_path = Path(repo_dir)
                if repo_path.exists() and repo_path.is_dir():
                    for ili_file in repo_path.glob('*.ili'):
                        model_name = ili_file.stem
                        self.local_models[model_name] = ili_file
                else:
                    print(f"Warning: Local repository directory '{repo_dir}' not found or not a directory.")
    
    def _load_model(self, model_path: Optional[str] = None):
        """
        Load and index an INTERLIS model from local file or stream.
        
        Args:
            model_path: Path to the .ili model file. If None, uses self.model_path
        """
        path_value = model_path if model_path is not None else self.model_path_raw
        
        if not path_value:
            return
        
        try:
            # Lazy import to avoid circular dependencies
            from .parser import parse_ili_model, parse_ili_model_text
            
            # Parse the ILI model
            if self._is_url(path_value):
                with urlopen(path_value) as response:
                    content = response.read().decode("utf-8", errors="replace")
                models = parse_ili_model_text(content)
            else:
                models = parse_ili_model(str(Path(path_value)))
            if not models:
                raise ValueError(f"Failed to parse model from {path_value}")
            # Always treat models as a list
            if not isinstance(models, list):
                models = [models]
            # Index all models from the .ili file
            for model in models:
                model_name = model.name
                self.models[model_name] = model
                print(f"DEBUG: Indexed model '{model_name}' from file")
                # Debug: print loaded model name, URI, version
                print(f"DEBUG: Loaded model '{model_name}' URI={getattr(model, 'at', None)} VERSION={getattr(model, 'version', None)}")
                # Set primary model only if not already set
                if not self.model:
                    self.model = model
                # Index classes and topics for quick lookup
                if hasattr(model, 'topics'):
                    for topic in model.topics:
                        topic_key = f"{model_name}.{topic.name}"
                        self.topics_by_name[topic_key] = topic
                        self.topics_by_name[topic.name] = topic  # Also index by simple name
                        # Index classes within each topic
                        if hasattr(topic, 'classes'):
                            for cls in topic.classes:
                                self.classes_by_name[cls.name] = cls
                                qualified_name = f"{model_name}.{topic.name}.{cls.name}"
                                self.classes_by_name[qualified_name] = cls
        except Exception as e:
            raise ValueError(f"Failed to load model {path_value}: {e}")

    @staticmethod
    def _is_url(value: str) -> bool:
        parsed = urlparse(value)
        return parsed.scheme in ("http", "https")
    
    def _load_model_from_stream(self, model_name: str, content: str) -> bool:
        """
        Load and index a model from stream content.
        
        Args:
            model_name: Name of the model
            content: Model content as string
            
        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            from .parser import parse_ili_model
            import tempfile
            from pathlib import Path
            
            # Parse model from string content
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.ili', delete=False, encoding='utf-8')
            temp_file.write(content)
            temp_path = temp_file.name
            temp_file.close()
            
            try:
                models = parse_ili_model(temp_path)
                if not models:
                    return False
                if not isinstance(models, list):
                    models = [models]
                for model in models:
                    actual_model_name = model.name
                    self.models[actual_model_name] = model
                    # Also register under requested name if different (alias)
                    if model_name != actual_model_name:
                        self.models[model_name] = model
                    # Index classes and topics
                    if hasattr(model, 'topics'):
                        for topic in model.topics:
                            topic_key = f"{actual_model_name}.{topic.name}"
                            self.topics_by_name[topic_key] = topic
                            self.topics_by_name[topic.name] = topic
                            if hasattr(topic, 'classes'):
                                for cls in topic.classes:
                                    self.classes_by_name[cls.name] = cls
                                    qualified_name = f"{actual_model_name}.{topic.name}.{cls.name}"
                                    self.classes_by_name[qualified_name] = cls
                return True
            finally:
                Path(temp_path).unlink(missing_ok=True)
        except Exception as e:
            return False
    
    def _extract_namespace_prefixes(self, xtf_doc: XTFDocument) -> Dict[str, str]:
        """
        Extract namespace prefixes to model names from XTF document.
        
        Parses XML namespace declarations to map prefixes like 'DMAV_Dienstbarkeitsgrenzen_V1_0'
        to their corresponding model names.
        
        Args:
            xtf_doc: Parsed XTF document
            
        Returns:
            Dictionary mapping namespace prefix -> model name
        """
        ns_to_model = {}
        
        if not xtf_doc.raw_tree:
            return ns_to_model
        
        root = xtf_doc.raw_tree.getroot()
        
        # Extract namespace declarations
        for prefix, uri in root.attrib.items():
            # Handle xmlns:prefix format
            if prefix.startswith('{http://www.w3.org/2000/xmlns/}'):
                ns_prefix = prefix.split('}')[1]
                # The URI might contain the model name or it might be a namespace URI
                # Try to extract model name from prefix (e.g., DMAV_Dienstbarkeitsgrenzen_V1_0)
                if ns_prefix and ns_prefix[0].isupper():
                    # Likely a model prefix, extract model name
                    # Remove version suffix if present (V1_0, V2_1, etc.)
                    model_name = self._extract_model_name_from_prefix(ns_prefix)
                    if model_name:
                        ns_to_model[ns_prefix] = model_name
        
        return ns_to_model
    
    def _extract_model_name_from_prefix(self, prefix: str) -> Optional[str]:
        """
        Extract model name from namespace prefix.
        
        Examples:
            DMAV_Dienstbarkeitsgrenzen_V1_0 -> DMAV_Dienstbarkeitsgrenzen_V1_0
            StandardSymbology_V2_4 -> StandardSymbology_V2_4
        
        Args:
            prefix: Namespace prefix
            
        Returns:
            Model name or None
        """
        if not prefix:
            return None
        
        # The prefix itself is typically the model name (with version suffix)
        # Try to find it in header models first
        return prefix
    
    def validate(self, xtf_path: str) -> ValidationResult:
        """
        Validate an XTF file against the loaded model(s).
        
        If no model was provided at initialization, will auto-discover models
        from the XTF header and namespace prefixes.
        
        Args:
            xtf_path: Path to the .xtf file
            
        Returns:
            ValidationResult with validation status and errors
        """
        result = ValidationResult(is_valid=True)
        
        try:
            # Parse the XTF file
            xtf_doc = parse_xtf(xtf_path)

            # Auto-discover models if not already loaded
            if not self.models:
                self._discover_and_load_models(xtf_doc, result)

            # Only load catalog files if there are catalog TIDs referenced in the XTF data
            referenced_catalog_tids = set()
            for basket in xtf_doc.baskets:
                for obj in basket.objects:
                    for ref_tid in obj.references.values():
                        referenced_catalog_tids.add(ref_tid)
            if referenced_catalog_tids:
                self._load_catalog_files(xtf_path, xtf_doc, result)

            # Validate header
            self._validate_header(xtf_doc, result)

            # Validate baskets and objects
            self._validate_baskets(xtf_doc, result)

            # Validate references (including catalog references)
            self._validate_references(xtf_doc, result)

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            result.add_error(f"Failed to validate XTF file: {e}\n{tb}")

        return result
    
    def _discover_and_load_models(self, xtf_doc: XTFDocument, result: ValidationResult):
        """
        Discover and load models referenced in the XTF file.
        
        Uses multiple strategies:
        1. Models listed in XTF header
        2. Namespace prefixes to identify model names
        3. Local files
        4. Streaming from remote repositories (using metadata index)
        
        Args:
            xtf_doc: Parsed XTF document
            result: Validation result to add info/warning messages
        """
        models_to_load = set()
        
        # Add models from XTF header
        header_models = set()
        if xtf_doc.header.models:
            header_models.update(xtf_doc.header.models)
            result.add_info(f"XTF references {len(xtf_doc.header.models)} models in header")
        
        # Extract models from namespace prefixes in baskets (data section)
        namespace_models = self._extract_models_from_baskets(xtf_doc)
        if namespace_models:
            # Prefer models actually used in data section
            models_to_load.update(namespace_models)
            if header_models and namespace_models != header_models:
                skipped = header_models - namespace_models
                # Skip info message about header-only models
        else:
            # Fallback to header models if no data-section models were found
            models_to_load.update(header_models)
        
        # If repositories are available, use ilimodels.xml to locate models
        # Only consider models actually used in the data section
        if self.streaming_loader and self.streaming_loader.indices and header_models:
            models_to_check = namespace_models if namespace_models else header_models
            any_metadata_loaded = any(index.loaded for index in self.streaming_loader.indices.values())
            for model_name in sorted(models_to_check):
                model_url = self.streaming_loader.find_model_url(model_name)
                if model_url:
                    result.add_info(
                        f"Model '{model_name}' located in repository: {model_url}"
                    )
                else:
                    if any_metadata_loaded:
                        result.add_warning(
                            f"Model '{model_name}' not listed in repository metadata"
                        )
                    else:
                        result.add_info(
                            f"Repository metadata not available to locate model '{model_name}'"
                        )
        
        # Try to load each discovered model
        loaded_count = 0
        failed_models = []
        
        for model_name in models_to_load:
            if model_name in self.models:
                loaded_count += 1
                # (matched variable is no longer used; skip this check)
            # Strategy 1: Load from local path if provided
            if self.model_path and self.model_path.parent.exists():
                local_path = self.model_path.parent / f"{model_name}.ili"
                if local_path.exists():
                    try:
                        self._load_model(str(local_path))
                        loaded_count += 1
                        continue
                    except Exception as e:
                        result.add_warning(f"Failed to load model from {local_path}: {e}")
            
            # Strategy 2: Stream from remote repositories (no disk caching)
            if self.streaming_loader:
                content = self.streaming_loader.stream_model_content(model_name)
                if content:
                    if self._load_model_from_stream(model_name, content):
                        loaded_count += 1
                        result.add_info(f"Streamed model '{model_name}' from remote repository")
                        continue
            
            # Strategy 3: Try to resolve from remote repositories (fallback)
            resolved_url = self._try_resolve_remote_model(
                model_name,
                xtf_doc.header.model_refs,
                result,
            )
            
            if resolved_url:
                loaded_count += 1
            else:
                failed_models.append(model_name)
        
        # Repository info available but not logged to reduce verbosity
        
        # Different behavior based on context:
        # 1. If using streaming repos and models still missing: ERROR
        # 2. If in pure auto-discovery (no repo): WARNING
        # 3. If we have NO models at all: ERROR
        
        if failed_models:
            if self.streaming_loader and self.streaming_loader.indices:
                # We have repos configured but still missing models - this is an error
                for model_name in failed_models[:5]:
                    result.add_error(f"Could not find or load model '{model_name}'")
                if len(failed_models) > 5:
                    result.add_error(
                        f"Additional models not found: {len(failed_models) - 5}"
                    )
            elif not self.models:
                # Pure auto-discovery with no models found - report as warnings instead of errors
                result.add_warning(f"Could not load any models. To validate, provide:")
                result.add_warning(f"  1. A model file: python cli.py model.ili --validate-xtf data.xtf")
                result.add_warning(f"  2. Or a remote repository: python cli.py --validate-xtf data.xtf --model-repo https://repo/")
                result.add_warning(f"  Missing models: {', '.join(failed_models[:5])}{'...' if len(failed_models) > 5 else ''}")
    
    def _extract_models_from_baskets(self, xtf_doc: XTFDocument) -> Set[str]:
        """
        Extract model names from basket namespace prefixes.
        
        Args:
            xtf_doc: Parsed XTF document
            
        Returns:
            Set of model names found in namespace prefixes
        """
        models = set()
        
        for basket in xtf_doc.baskets:
            # Topic name format: ModelName.TopicName
            if '.' in basket.topic_name:
                model_name = basket.topic_name.split('.')[0]
                models.add(model_name)
            
            for obj in basket.objects:
                # Class name format might be ModelName.TopicName.ClassName or just ClassName
                if '.' in obj.class_name:
                    parts = obj.class_name.split('.')
                    if len(parts) >= 2:
                        model_name = parts[0]
                        models.add(model_name)
        
        return models
    
    def _load_catalog_files(self, xtf_path: str, xtf_doc: XTFDocument, result: ValidationResult):
        """
        Detect and load catalog files associated with the XTF file.
        
        Looks for catalog files in the same directory with patterns:
        - *_Catalogue_*.xml
        - *_Catalog_*.xml
        - *Catalogue*.xml
        - *Catalog*.xml
        
        Args:
            xtf_path: Path to the XTF file being validated
            xtf_doc: Parsed XTF document
            result: Validation result to add info messages
        """
        from .xtf_parser import XTFParser
        
        xtf_file = Path(xtf_path)
        xtf_dir = xtf_file.parent
        xtf_stem = xtf_file.stem
        
        # Patterns to search for catalog files
        catalog_patterns = [
            f"{xtf_stem}_Catalogue_*.xml",
            f"{xtf_stem}_Catalog_*.xml",
            f"{xtf_stem}-catalogs.xml",
            f"{xtf_stem}-catalogues.xml",
            f"*_Catalogue_*.xml",
            f"*_Catalog_*.xml",
            f"*-catalogs.xml",
            f"*-catalogues.xml",
            f"*Catalogue*.xml",
            f"*Catalog*.xml",
        ]
        
        catalog_files = set()
        for pattern in catalog_patterns:
            catalog_files.update(xtf_dir.glob(pattern))
        
        # Remove the XTF file itself if it matched
        catalog_files.discard(xtf_file)
        
        if catalog_files:
            result.add_info(f"Found {len(catalog_files)} catalog file(s): {', '.join(f.name for f in catalog_files)}")
        
        # Parse each catalog file
        parser = XTFParser()
        for catalog_file in catalog_files:
            try:
                catalog_items = parser.parse_catalog_file(str(catalog_file))
                if catalog_items:
                    # Add to validator's catalog items
                    self.catalog_items.update(catalog_items)
                    # Also add to document's catalog items
                    xtf_doc.catalog_items.update(catalog_items)
                    result.add_info(f"Loaded {len(catalog_items)} catalog items from {catalog_file.name}")
            except Exception as e:
                result.add_warning(f"Failed to parse catalog file {catalog_file.name}: {e}")
        # After loading all catalog files, print referenced catalog TIDs in XTF
        referenced_catalog_tids = set()
        for basket in xtf_doc.baskets:
            for obj in basket.objects:
                for ref_tid in obj.references.values():
                    referenced_catalog_tids.add(ref_tid)
        print(f"DEBUG: Catalog TIDs referenced in XTF: {sorted(referenced_catalog_tids)}")
    
    def _validate_header(self, xtf_doc: XTFDocument, result: ValidationResult):
        """Validate the XTF header section."""
        header_models = xtf_doc.header.models
        header_models_ci = {m.lower() for m in header_models}
        data_models = self._extract_models_from_baskets(xtf_doc)
        
        # Check models in header
        if not header_models:
            result.add_info("XTF header contains no explicit model references (may be auto-discovered from namespaces)")
        else:
            result.add_info(f"XTF file references models: {', '.join(header_models)}")
        
        # Verify that referenced models are available
        # Only consider models actually used in the data section
        loaded_model_names = set(self.models.keys())
        loaded_model_names_ci = {m.lower() for m in loaded_model_names}
        for model_name in header_models:
            if data_models and model_name not in data_models:
                continue
            # Improved: treat model as available if present in loaded models (case-insensitive)
            loaded_model_names_ci = {m.lower() for m in self.models.keys()}
            if model_name.lower() in loaded_model_names_ci:
                continue  # Model is loaded, skip warning
            # Try to resolve remotely if not found
            resolved = self._try_resolve_remote_model(
                model_name,
                xtf_doc.header.model_refs,
                result,
            )
            loaded_model_names_ci = {m.lower() for m in self.models.keys()}
            if model_name.lower() in loaded_model_names_ci:
                continue  # Model is loaded after resolve
            if not resolved:
                if self.streaming_loader and self.streaming_loader.indices:
                    loaded_models = ", ".join(self.models.keys())
                    if not loaded_models:
                        loaded_models = "(none)"
                    result.add_error(
                        f"Model '{model_name}' in XTF header not found. "
                        f"Loaded models: {loaded_models}"
                    )
                elif self.models:
                    result.add_warning(
                        f"Model '{model_name}' in XTF header not available. "
                        f"Available: {', '.join(list(self.models.keys())[:3])}..."
                    )
            # (matched variable is no longer used; skip this check)
            if not resolved:
                # Only report as error if we have streaming repos configured
                # (meaning we tried and failed to find it)
                if self.streaming_loader and self.streaming_loader.indices:
                    loaded_models = ", ".join(self.models.keys())
                    if not loaded_models:
                        loaded_models = "(none)"
                    result.add_error(
                        f"Model '{model_name}' in XTF header not found. "
                        f"Loaded models: {loaded_models}"
                    )
                # Otherwise in pure auto-discovery mode, just log for debugging
                elif self.models:  # We have some models, but not this one
                    result.add_warning(
                        f"Model '{model_name}' in XTF header not available. "
                        f"Available: {', '.join(list(self.models.keys())[:3])}..."
                    )
        
        if xtf_doc.header.sender:
            result.add_info(f"Created by: {xtf_doc.header.sender}")

    def _try_resolve_remote_model(
        self,
        model_name: str,
        model_refs: List[XTFModelRef],
        result: ValidationResult,
    ) -> Optional[str]:
        """
        Try to resolve a model name using remote repositories.

        Returns the URL used if successful, otherwise None.
        """
        candidate_urls: List[str] = []

        checked_bases: Set[str] = set()

        # Use header model refs URIs if provided
        for ref in model_refs:
            if not ref.uri:
                continue
            base = self._normalize_repo_base(ref.uri)
            if base in checked_bases:
                continue
            checked_bases.add(base)
            if not self._check_repo_index_files(base, result):
                continue
            candidate_urls.append(self._build_model_url(base, ref.name))

        # Use user-provided repositories
        for repo in self.model_repositories:
            if not repo:
                continue
            base = self._normalize_repo_base(repo)
            if base in checked_bases:
                continue
            checked_bases.add(base)
            if not self._check_repo_index_files(base, result):
                continue
            candidate_urls.append(self._build_model_url(base, model_name))

        for url in candidate_urls:
            local_path = self._download_model(url, model_name)
            if local_path and self._matches_model_name(local_path, model_name):
                return url

        return None

    def _normalize_repo_base(self, uri: str) -> str:
        """
        Normalize a repository base URL to the repository root.
        
        Extracts the scheme and netloc from the given URI, returning the root
        repository URL where index files (ilimodels.xml, ilisite.xml, ilidata.xml)
        are located.
        
        Examples:
            https://models.geo.admin.ch/ARE/RoadTrafficCensus.ili
            -> https://models.geo.admin.ch
            
            https://models.interlis.ch/INTERLIS/Core.ili
            -> https://models.interlis.ch
            
            http://example.com/models/subdir/mymodel.ili
            -> http://example.com
        
        Args:
            uri: A model URI or repository URL (may include path and .ili file)
        
        Returns:
            The repository root URL (scheme + netloc)
        """
        parsed = urllib.parse.urlparse(uri)
        
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
        
        # Fallback for non-URL formats
        return uri.rstrip('/')

    def _build_model_url(self, base: str, model_name: str) -> str:
        return urllib.parse.urljoin(f"{base}/", f"{model_name}.ili")

    def _check_repo_index_files(self, base: str, result: ValidationResult) -> bool:
        """Ensure required index files exist at the repository root."""
        required = ["ilimodels.xml", "ilisite.xml"]
        optional = ["ilidata.xml"]

        missing_required = []
        for filename in required:
            url = urllib.parse.urljoin(f"{base}/", filename)
            if not self._url_exists(url):
                missing_required.append(filename)

        if missing_required:
            # Skip remote repository validation errors - they are optional
            # (repositories may not always be available or reachable)
            return False

        # Optional file for object catalogs
        for filename in optional:
            url = urllib.parse.urljoin(f"{base}/", filename)
            if not self._url_exists(url):
                pass  # Optional file missing is expected, don't log

        return True

    def _url_exists(self, url: str) -> bool:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as response:
                return 200 <= response.status < 300
        except Exception:
            # Fallback to GET for servers that don't support HEAD
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    return 200 <= response.status < 300
            except Exception:
                return False

    def _download_model(self, url: str, model_name: str) -> Optional[Path]:
        """
        Download a model file to a local cache and return its path.
        
        Note: When using streaming from remote repositories, prefer to stream
        directly instead of downloading and caching.
        """
        # If no local model path specified, don't cache (use streaming instead)
        if not self.model_path:
            return None
        
        cache_dir = self.model_path.parent / ".interlis_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        target_path = cache_dir / f"{model_name}.ili"

        if target_path.exists():
            return target_path

        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                if response.status != 200:
                    return None
                content = response.read()
            target_path.write_bytes(content)
            return target_path
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
            return None

    def _matches_model_name(self, model_path: Path, model_name: str) -> bool:
        """Parse a model file and check its declared name."""
        try:
            from .parser import parse_ili_model
            parsed = parse_ili_model(str(model_path))
            return bool(parsed and getattr(parsed, "name", "").lower() == model_name.lower())
        except Exception:
            return False
    
    def _validate_baskets(self, xtf_doc: XTFDocument, result: ValidationResult):
        """Validate all baskets and their objects."""
        # Skip validation if we have no models loaded
        if not self.models:
            # Only error if we explicitly expected to load models (streaming_loader or model_path provided)
            if self.streaming_loader or self.model_path:
                result.add_error("No models loaded - cannot validate baskets")
            else:
                result.add_warning("No models loaded - skipping basket validation")
            return
        
        for basket in xtf_doc.baskets:
            # Validate basket topic exists in appropriate model
            topic_name = basket.topic_name
            
            # Find the model for this basket
            # Topic name format: ModelName.TopicName
            if '.' in topic_name:
                model_name, topic_simple = topic_name.split('.', 1)
            else:
                # Try to infer from objects
                model_name = None
                if basket.objects:
                    obj = basket.objects[0]
                    if '.' in obj.class_name:
                        model_name = obj.class_name.split('.')[0]
                topic_simple = topic_name
            instantiated_models = set()  # Initialize a set to collect model names
            for basket in xtf_doc.baskets:
                # Topic name format: Model.Topic
                topic_name = basket.topic_name
                if '.' in topic_name:
                    model_name = topic_name.split('.', 1)[0]
                    instantiated_models.add(model_name)
                # Also check object class names for model prefix
                for obj in basket.objects:
                    if '.' in obj.class_name:
                        model_name = obj.class_name.split('.', 1)[0]
                        instantiated_models.add(model_name)

            # Step 2: Load only instantiated models and resolve dependencies
            # Use streaming loader and repository index, or local repositories
            loaded_models = set()
            to_load = set(instantiated_models)
            while to_load:
                model_name = to_load.pop()
                if model_name in loaded_models:
                    continue
                # Try local repository first
                if model_name in self.local_models:
                    ili_path = self.local_models[model_name]
                    self._load_model(str(ili_path))
                    loaded_models.add(model_name)
                    continue
                # Try remote streaming loader
                if self.streaming_loader:
                    model_url = self.streaming_loader.find_model_url(model_name)
                    if model_url:
                        model_content = self.streaming_loader.stream_model_content(model_name)
                        if model_content:
                            self._load_model_from_stream(model_name, model_content)
                            loaded_models.add(model_name)
                            # Resolve dependencies from ilimodels.xml
                            index = self.streaming_loader.indices.get(self.streaming_loader.find_model_url(model_name).rsplit('/', 1)[0])
                            if index and index.has_model(model_name):
                                for basket in xtf_doc.baskets:
                                    topic_name = basket.topic_name
                                    # Topic name format: ModelName.TopicName
                                    if '.' in topic_name:
                                        model_name, topic_simple = topic_name.split('.', 1)
                                    else:
                                        # Try to infer from objects
                                        model_name = None
                                        if basket.objects:
                                            obj = basket.objects[0]
                                            if '.' in obj.class_name:
                                                model_name = obj.class_name.split('.')[0]
                                        topic_simple = topic_name

                                    # Try to find the correct model for the topic
                                    model = None
                                    if model_name and model_name in self.models:
                                        model = self.models[model_name]
                                    else:
                                        # Search all loaded models for topic
                                        for m in self.models.values():
                                            if hasattr(m, 'topics'):
                                                for t in m.topics:
                                                    if t.name == topic_simple:
                                                        model = m
                                                        break
                                                if model:
                                                    break

                                    if not model:
                                        result.add_warning(
                                            f"Model for basket '{basket.bid}' with topic '{topic_simple}' not loaded. Skipping validation. "
                                            f"(Available: {', '.join(list(self.models.keys())[:3])}...)"
                                        )
                                        continue

                                    # Check if topic exists in model
                                    topic_found = False
                                    if hasattr(model, 'topics'):
                                        for topic in model.topics:
                                            if topic.name == topic_simple:
                                                topic_found = True
                                                break

                                    if not topic_found:
                                        result.add_warning(
                                            f"Topic '{topic_simple}' in basket {basket.bid} not found in model '{model.name}'. "
                                            f"Skipping validation for this basket."
                                        )
                                        continue

                                    # Validate each object in the basket
                                    for obj in basket.objects:
                                        self._validate_object(obj, topic_name, model, result)

            # Removed leftover attribute validation code; attribute validation is handled in _validate_attributes and _validate_object
    
    def _validate_attribute_value(self, attr: Any, value: Any, obj: XTFObject, result: ValidationResult):
        # Helper to check decimal digits
        def count_decimals(val):
            try:
                s = str(val)
                if '.' in s:
                    return len(s.split('.')[-1])
                return 0
            except Exception:
                return 0

        # For CHLV95, coordinates must have exactly 3 decimals
        def check_coord_decimals(axis, axis_val):
            decimals = count_decimals(axis_val)
            if decimals != 3:
                result.add_error(
                    f"Coordinate axis '{axis}' in attribute '{attr.name}' must have exactly 3 decimal digits (found {decimals}): {axis_val}",
                    object_tid=obj.tid,
                    attribute_name=attr.name
                )

        # Recursively check all COORD elements in XML
        def recursive_coord_check(elem):
            import xml.etree.ElementTree as ET
            if isinstance(elem, ET.Element):
                tag = elem.tag.split('}', 1)[-1] if '}' in elem.tag else elem.tag
                if tag == 'COORD':
                    for child in elem:
                        axis = child.tag.split('}', 1)[-1] if '}' in child.tag else child.tag
                        axis_val = child.text.strip() if child.text else ''
                        try:
                            float(axis_val)
                            check_coord_decimals(axis, axis_val)
                        except (ValueError, TypeError):
                            result.add_error(
                                f"Invalid numeric value for COORD axis '{axis}' in attribute '{attr.name}': {axis_val}",
                                object_tid=obj.tid,
                                attribute_name=attr.name
                            )
                # Recurse into all children
                for child in elem:
                    recursive_coord_check(child)

        import xml.etree.ElementTree as ET
        # Handle COORD structure: dicts or XML elements
        if isinstance(value, dict):
            # If value is a dict with a single key 'COORD', descend into it
            if set(value.keys()) == {'COORD'}:
                coord_val = value['COORD']
                # If COORD is a dict, validate axes
                if isinstance(coord_val, dict):
                    for axis, axis_val in coord_val.items():
                        try:
                            float(axis_val)
                            check_coord_decimals(axis, axis_val)
                        except (ValueError, TypeError):
                            result.add_error(
                                f"Invalid numeric value for COORD axis '{axis}' in attribute '{attr.name}': {axis_val}",
                                object_tid=obj.tid,
                                attribute_name=attr.name
                            )
                # If COORD is an XML element, extract axes recursively
                elif isinstance(coord_val, ET.Element):
                    recursive_coord_check(coord_val)
            else:
                # COORD-like dicts (e.g., {'C1': ..., 'C2': ...})
                for axis, axis_val in value.items():
                    try:
                        float(axis_val)
                        check_coord_decimals(axis, axis_val)
                    except (ValueError, TypeError):
                        result.add_error(
                            f"Invalid numeric value for COORD axis '{axis}' in attribute '{attr.name}': {axis_val}",
                            object_tid=obj.tid,
                            attribute_name=attr.name
                        )
        elif isinstance(value, ET.Element):
            # Recursively check all COORD elements in the XML tree
            recursive_coord_check(value)

        # Continue with normal type validation below (in case further constraints apply)
        if not hasattr(attr, 'type_') or not attr.type_:
            return
        # Lazy import to avoid circular dependencies
        from .types import TextType, NumericType, EnumerationType
        domain = attr.type_
        # Text type validation
        if isinstance(domain, TextType):
            if hasattr(domain, 'max_length') and domain.max_length:
                if len(str(value)) > domain.max_length:
                    result.add_error(
                        f"Text value too long for attribute '{attr.name}': "
                        f"{len(str(value))} > {domain.max_length}",
                        object_tid=obj.tid,
                        attribute_name=attr.name
                    )
        # Numeric type validation
        elif isinstance(domain, NumericType):
            try:
                num_value = float(value)
                if hasattr(domain, 'min_value') and domain.min_value is not None:
                    min_val = float(domain.min_value)
                    if num_value < min_val:
                        result.add_error(
                            f"Numeric value too small for attribute '{attr.name}': "
                            f"{num_value} < {min_val}",
                            object_tid=obj.tid,
                            attribute_name=attr.name
                        )
                if hasattr(domain, 'max_value') and domain.max_value is not None:
                    max_val = float(domain.max_value)
                    if num_value > max_val:
                        result.add_error(
                            f"Numeric value too large for attribute '{attr.name}': "
                            f"{num_value} > {max_val}",
                            object_tid=obj.tid,
                            attribute_name=attr.name
                        )
            except (ValueError, TypeError):
                result.add_error(
                    f"Invalid numeric value for attribute '{attr.name}': {value}",
                    object_tid=obj.tid,
                    attribute_name=attr.name
                )
        # Enumeration type validation
        elif isinstance(domain, EnumerationType):
            if hasattr(domain, 'values') and domain.values:
                if value not in domain.values:
                    result.add_error(
                        f"Invalid enumeration value for attribute '{attr.name}': "
                        f"'{value}' not in {domain.values}",
                        object_tid=obj.tid,
                        attribute_name=attr.name
                    )
    
    def _validate_references(self, xtf_doc: XTFDocument, result: ValidationResult):
        """Validate that all references point to existing objects (in document or catalogs)."""
        # Collect all TIDs in the document
        all_tids: Set[str] = set()
        for basket in xtf_doc.baskets:
            for obj in basket.objects:
                all_tids.add(obj.tid)

        # Add catalog item TIDs from both validator and document
        catalog_tids = set(self.catalog_items.keys())
        catalog_tids_doc = set(xtf_doc.catalog_items.keys())
        all_tids.update(catalog_tids)
        all_tids.update(catalog_tids_doc)

        # Log catalog TID count for debugging
        result.add_info(f"Catalog TIDs loaded: {len(catalog_tids)} (validator), {len(catalog_tids_doc)} (document)")

        # Validate each reference
        for basket in xtf_doc.baskets:
            for obj in basket.objects:
                for ref_name, ref_tid in obj.references.items():
                    if ref_tid not in all_tids:
                        result.add_error(
                            f"Reference '{ref_name}' points to non-existent object: {ref_tid} "
                            f"(not found in data or catalog files)",
                            object_tid=obj.tid,
                            attribute_name=ref_name
                        )
                    elif ref_tid in catalog_tids or ref_tid in catalog_tids_doc:
                        # Reference points to catalog item - this is valid
                        pass


def validate_xtf(xtf_path: str, model_path: Optional[str] = None,
                 model_repositories: Optional[List[str]] = None,
                 local_repositories: Optional[List[str]] = None) -> ValidationResult:
    """
    Convenience function to validate an XTF file against model(s).
    
    Args:
        xtf_path: Path to the .xtf file
        model_path: Optional path to a .ili model file. If not provided, models will be
                   auto-discovered from the XTF header and namespace prefixes.
        model_repositories: Optional list of remote model repository base URLs
        local_repositories: Optional list of local model repository directories
        
    Returns:
        ValidationResult with validation status
        
    Example:
        >>> # Validate with explicit model
        >>> result = validate_xtf("input/myData.xtf", "input/myModel.ili")
        >>> 
        >>> # Validate with auto-discovered models
        >>> result = validate_xtf("input/myData.xtf")
        >>> 
        >>> if result.is_valid:
        ...     print("Validation passed!")
        ... else:
        ...     for error in result.errors:
        ...         print(error)
    """
    validator = XTFValidator(model_path, model_repositories=model_repositories, local_repositories=local_repositories)
    return validator.validate(xtf_path)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 2:
        xtf_file = sys.argv[1]
        ili_file = sys.argv[2]
        
        print(f"Validating {xtf_file} against {ili_file}...")
        result = validate_xtf(xtf_file, ili_file)
        
        print(f"\n{result.summary()}\n")
        
        if result.errors:
            print("ERRORS:")
            for error in result.errors:
                print(f"  {error}")
        
        if result.warnings:
            print("\nWARNINGS:")
            for warning in result.warnings:
                print(f"  {warning}")
        
        if result.info:
            print("\nINFO:")
            for info in result.info:
                print(f"  {info}")
        
        sys.exit(0 if result.is_valid else 1)
    else:
        print("Usage: python xtf_validator.py <xtf_file> <ili_file>")
        sys.exit(1)
