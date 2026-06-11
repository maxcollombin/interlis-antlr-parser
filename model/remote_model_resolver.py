"""
Remote Model Resolver - Stream INTERLIS models from repositories without caching

This module provides functionality to:
1. Query repository metadata (ilimodels.xml, ilisite.xml)
2. Stream model files directly from HTTP
3. Parse models without writing to disk
"""

import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, Optional, List, Set
from dataclasses import dataclass
from pathlib import Path
import io


@dataclass
class ModelMetadata:
    """Metadata about a model from ilimodels.xml"""
    name: str
    version: Optional[str] = None
    file: Optional[str] = None  # Relative path to .ili file
    repository_uri: Optional[str] = None


class RemoteModelIndex:
    """Parses and manages model metadata from repository indices"""
    
    def __init__(self, repository_url: str):
        """
        Initialize remote model index.
        
        Args:
            repository_url: Base URL of the repository (e.g., https://models.example.com)
        """
        self.repository_url = repository_url.rstrip('/')
        self.models: Dict[str, ModelMetadata] = {}
        self.loaded = False
        self.last_error: Optional[str] = None
    
    def load_metadata(self) -> bool:
        """
        Load model metadata from ilimodels.xml
        
        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            candidate_bases = self._candidate_repository_bases(self.repository_url)
            last_error = None
            for base in candidate_bases:
                metadata_url = f"{base.rstrip('/')}/ilimodels.xml"
                try:
                    self._parse_ilimodels_xml(metadata_url)
                    self.repository_url = base.rstrip('/')
                    self.loaded = True
                    self.last_error = None
                    return True
                except Exception as e:
                    last_error = e
                    continue

            if last_error:
                self.last_error = str(last_error)
            self.loaded = False
            return False
        except Exception as e:
            self.last_error = str(e)
            self.loaded = False
            return False

    def _candidate_repository_bases(self, base_url: str) -> List[str]:
        """
        Build candidate repository base URLs by walking up the path.

        Example:
          http://www.interlis.ch/xtf/2.4/ ->
          [http://www.interlis.ch/xtf/2.4/, http://www.interlis.ch/xtf/]
        """
        base = base_url.rstrip('/')
        candidates = [base + '/']

        # Walk up to two levels to find ilimodels.xml
        for _ in range(2):
            if '/' not in base:
                break
            base = base.rsplit('/', 1)[0]
            if base.startswith('http'):
                candidates.append(base + '/')

        # Deduplicate while preserving order
        seen = set()
        ordered = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                ordered.append(c)
        return ordered
    
    def _parse_ilimodels_xml(self, url: str):
        """
        Parse ilimodels.xml (which is actually an XTF transfer file with INTERLIS data).
        
        The file structure is:
        ```xml
        <TRANSFER xmlns="http://www.interlis.ch/INTERLIS2.3">
          <DATASECTION>
            <IliRepository09.RepositoryIndex>
              <IliRepository09.RepositoryIndex.ModelMetadata TID="1">
                <Name>ModelName</Name>
                <File>path/to/Model.ili</File>
                <Version>1.0</Version>
              </IliRepository09.RepositoryIndex.ModelMetadata>
            </IliRepository09.RepositoryIndex>
          </DATASECTION>
        </TRANSFER>
        ```
        
        Args:
            url: URL to ilimodels.xml
        """
        with urllib.request.urlopen(url, timeout=10) as response:
            content = response.read()
        
        root = ET.fromstring(content)
        
        # Handle namespace - the file uses INTERLIS 2.3 namespace
        ns = {'ili': 'http://www.interlis.ch/INTERLIS2.3'}
        
        # Find all ModelMetadata elements (can appear in different structures)
        # Look for elements ending with "ModelMetadata"
        for elem in root.iter():
            # Check if this is a ModelMetadata element
            if 'ModelMetadata' in elem.tag:
                name = None
                file = None
                version = None
                
                # Extract metadata from child elements
                for child in elem:
                    tag_name = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                    
                    if tag_name == 'Name' and child.text:
                        name = child.text.strip()
                    elif tag_name == 'File' and child.text:
                        file = child.text.strip()
                    elif tag_name == 'Version' and child.text:
                        version = child.text.strip()
                
                if name and file:
                    self.models[name] = ModelMetadata(
                        name=name,
                        version=version,
                        file=file,
                        repository_uri=self.repository_url
                    )
    
    def _get_element_text(self, parent: ET.Element, tag: str) -> Optional[str]:
        """Extract text from child element (handles namespaces)"""
        # Try direct child first
        elem = parent.find(tag)
        if elem is not None and elem.text:
            return elem.text.strip()
        
        # Try with namespace wildcard
        for elem in parent.iter():
            if elem.tag.endswith('}' + tag) or elem.tag == tag:
                if elem.text:
                    return elem.text.strip()
        
        return None
    
    def has_model(self, model_name: str) -> bool:
        """Check if model exists in repository metadata"""
        return model_name in self.models
    
    def get_model_url(self, model_name: str) -> Optional[str]:
        """Get the download URL for a model"""
        metadata = self.models.get(model_name)
        if not metadata or not metadata.file:
            return None
        
        return urllib.parse.urljoin(f"{self.repository_url}/", metadata.file)
    
    def list_models(self) -> List[str]:
        """List all available models in the repository"""
        return list(self.models.keys())
    
    def available_models_count(self) -> int:
        """Get count of available models"""
        return len(self.models)


class StreamingModelLoader:
    """Load INTERLIS models directly from HTTP streams without caching"""
    
    def __init__(self):
        """Initialize streaming loader"""
        self.indices: Dict[str, RemoteModelIndex] = {}
        self.model_cache: Dict[str, any] = {}  # In-memory cache for current session
    
    def add_repository(self, repository_url: str) -> bool:
        """
        Add a repository and try to load its metadata index (optional).
        
        The metadata files (ilimodels.xml, ilidata.xml) are optional.
        If not available, the repository is still added and can be used
        for direct model URL construction (ModelName.ili).
        
        Args:
            repository_url: Base URL of repository
            
        Returns:
            True if repository added (metadata loaded or not available)
        """
        repository_url = repository_url.rstrip('/')
        
        if repository_url in self.indices:
            return True  # Already loaded
        
        index = RemoteModelIndex(repository_url)
        
        # Try to load metadata, but don't fail if it doesn't exist
        # The metadata is optional - we can still try direct URLs
        try:
            index.load_metadata()
            # Whether it succeeded or not, add the repository
        except Exception:
            # Metadata not available, but that's OK
            pass
        
        # Always add the repository, even if metadata isn't available
        self.indices[repository_url] = index
        return True
    
    def find_model_url(self, model_name: str) -> Optional[str]:
        """
        Find model URL across all registered repositories.
        
        Args:
            model_name: Name of model to find
            
        Returns:
            Full URL to model file, or None if not found
        """
        for index in self.indices.values():
            if index.has_model(model_name):
                url = index.get_model_url(model_name)
                if url:
                    return url
        
        return None
    
    def stream_model_content(self, model_name: str) -> Optional[str]:
        """
        Stream model content from remote repository without caching to disk.
        
        Tries multiple strategies:
        1. Look up URL in metadata index (if available)
        2. Try direct URL construction: ModelName.ili
        
        Args:
            model_name: Name of model to load
            
        Returns:
            Model file content as string, or None if not found
        """
        # Check in-memory cache first
        if model_name in self.model_cache:
            return self.model_cache[model_name]
        
        # Strategy 1: Find model URL from metadata index
        model_url = self.find_model_url(model_name)
        
        # Strategy 2: Try direct URL construction if metadata index doesn't have it
        # (in case ilimodels.xml wasn't available or didn't list the model)
        if not model_url:
            for repo_url in self.indices.keys():
                direct_url = f"{repo_url}/{model_name}.ili"
                try:
                    # Try to fetch from direct URL
                    with urllib.request.urlopen(direct_url, timeout=10) as response:
                        if 200 <= response.status < 300:
                            model_url = direct_url
                            break
                except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
                    # Try next repository
                    continue
        
        if not model_url:
            return None
        
        try:
            # Stream content from HTTP
            with urllib.request.urlopen(model_url, timeout=20) as response:
                content = response.read().decode('utf-8')
            
            # Cache in memory for this session
            self.model_cache[model_name] = content
            
            return content
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            return None
    
    def stream_model_file(self, model_name: str) -> Optional[io.StringIO]:
        """
        Stream model as file-like object for parsing.
        
        Args:
            model_name: Name of model to load
            
        Returns:
            StringIO object ready for parsing, or None if not found
        """
        content = self.stream_model_content(model_name)
        if not content:
            return None
        
        return io.StringIO(content)
    
    def get_available_repositories_info(self) -> List[Dict]:
        """Get information about loaded repositories and their models"""
        info = []
        for url, index in self.indices.items():
            info.append({
                'url': url,
                'loaded': index.loaded,
                'model_count': index.available_models_count(),
                'models_sample': index.list_models()[:5],
                'error': index.last_error
            })
        return info
    
    def discover_models_in_repositories(self) -> Set[str]:
        """
        Get all models available across all registered repositories.
        
        Returns:
            Set of model names
        """
        all_models = set()
        for index in self.indices.values():
            all_models.update(index.list_models())
        return all_models
    
    def clear_session_cache(self):
        """Clear in-memory cache for current session"""
        self.model_cache.clear()


def create_streaming_loader(repositories: List[str]) -> Optional[StreamingModelLoader]:
    """
    Create and initialize a streaming model loader with multiple repositories.
    
    Args:
        repositories: List of repository URLs
        
    Returns:
        StreamingModelLoader instance, or None if no repos loaded successfully
    """
    loader = StreamingModelLoader()
    
    for repo_url in repositories:
        if not loader.add_repository(repo_url):
            # Log warning but continue with other repos
            pass
    
    if loader.indices:
        return loader
    
    return None
