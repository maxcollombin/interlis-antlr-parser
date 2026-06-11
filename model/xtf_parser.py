"""
XTF Parser - Parse INTERLIS Transfer Files (.xtf)

This module provides functionality to parse INTERLIS Transfer Format (XTF) files
and extract their contents into Python data structures.

XTF files are XML-based transfer files that contain INTERLIS data instances
conforming to INTERLIS models (.ili files).
from shapely.geometry import Point, LineString

References: INTERLIS 2.4 Transfer Format Specification
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pathlib import Path


# XML namespace definitions for XTF files
NAMESPACES = {
    'ili': 'http://www.interlis.ch/xtf/2.4/INTERLIS',
    'geom': 'http://www.interlis.ch/geometry/1.0',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
}


@dataclass
class XTFHeader:
    """
    Header section of an XTF file containing metadata.
    
    Attributes:
        models: List of model names referenced in this transfer
        model_refs: List of model references with metadata
        sender: Application that created the transfer file
        comment: Optional comment about the transfer
    """
    models: List[str] = field(default_factory=list)
    model_refs: List['XTFModelRef'] = field(default_factory=list)
    sender: str = ""
    comment: Optional[str] = None


@dataclass
class XTFModelRef:
    """
    Model reference from XTF header.

    Attributes:
        name: Model name
        version: Model version (optional)
        uri: Model repository URI (optional)
    """
    name: str
    version: Optional[str] = None
    uri: Optional[str] = None


@dataclass
class XTFObject:
    """
    A single data object instance in an XTF file.
    
    Attributes:
        tid: Transfer ID (unique identifier)
        class_name: Fully qualified class name (e.g., 'myModel.Person')
        attributes: Dictionary of attribute name -> value
        references: Dictionary of reference attribute name -> TID
    """
    tid: str
    class_name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    references: Dict[str, str] = field(default_factory=dict)


@dataclass
class XTFBasket:
    """
    A basket (data container) in an XTF file.
    
    Attributes:
        bid: Basket ID
        topic_name: Topic name this basket belongs to
        objects: List of objects in this basket
    """
    bid: str
    topic_name: str
    objects: List[XTFObject] = field(default_factory=list)


@dataclass
class XTFDocument:
    """
    Complete representation of a parsed XTF file.
    
    Attributes:
        header: File header with metadata
        baskets: List of data baskets
        catalog_items: Dictionary of catalog item TID -> XTFObject (from external catalogs)
        raw_tree: Original XML tree (for advanced parsing)
    """
    header: XTFHeader
    baskets: List[XTFBasket] = field(default_factory=list)
    catalog_items: Dict[str, XTFObject] = field(default_factory=dict)
    raw_tree: Optional[ET.ElementTree] = None


class XTFParser:
    """Parser for INTERLIS Transfer Format (XTF) files."""
    
    def __init__(self):
        """Initialize the XTF parser."""
        self.namespaces = NAMESPACES.copy()
    
    def parse_file(self, file_path: str) -> XTFDocument:
        """
        Parse an XTF file and return its document structure.
        
        Args:
            file_path: Path to the .xtf file
            
        Returns:
            XTFDocument containing parsed header and baskets
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ET.ParseError: If XML is malformed
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"XTF file not found: {file_path}")
        
        try:
            tree = ET.parse(file_path)
        except ET.ParseError as e:
            # Try to fix unbound namespace prefixes by preprocessing the file
            # Read the file and extract all namespace prefixes used
            import re
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Find all namespace prefixes used in elements (e.g., prefix:element)
            used_prefixes = set(re.findall(r'<(\w+):', content))
            
            # Find all declared namespaces in root
            declared_prefixes = set(re.findall(r'xmlns:(\w+)=', content))
            
            # Find undeclared prefixes
            undeclared = used_prefixes - declared_prefixes
            
            if undeclared:
                # Add default namespace declarations for undeclared prefixes
                # Using the common INTERLIS pattern
                for prefix in undeclared:
                    ns_uri = f"http://www.interlis.ch/xtf/2.4/{prefix}"
                    content = content.replace(
                        '<ili:transfer',
                        f'<ili:transfer xmlns:{prefix}="{ns_uri}"',
                        1
                    )
            
            # Try parsing the fixed content
            try:
                from io import StringIO
                tree = ET.parse(StringIO(content))
            except ET.ParseError as parse_err:
                # If still failing, raise original error
                raise ET.ParseError(f"Cannot parse XTF file even after fixing namespaces: {str(e)}") from e
        
        root = tree.getroot()
        # (Debug prints removed for normal operation)

        # Update namespaces from root element
        self._update_namespaces(root)

        # Parse header section
        header = self._parse_header(root)

        # Parse data sections (baskets)
        baskets = self._parse_baskets(root)

        return XTFDocument(
            header=header,
            baskets=baskets,
            raw_tree=tree
        )
    
    def _update_namespaces(self, root: ET.Element):
        """
        Update namespace dictionary from root element.
        Extract all xmlns declarations including model-specific ones.
        
        Args:
            root: Root XML element
        """
        # Extract namespaces from root attributes (xmlns:prefix="uri")
        for attr_name, attr_value in root.attrib.items():
            if attr_name.startswith('{http://www.w3.org/2000/xmlns/}'):
                # Namespaced attribute xmlns:prefix
                ns_prefix = attr_name.split('}')[1]
                self.namespaces[ns_prefix] = attr_value
            elif attr_name.startswith('xmlns:'):
                # Direct xmlns:prefix attribute
                ns_prefix = attr_name.split(':')[1]
                self.namespaces[ns_prefix] = attr_value
            elif attr_name == 'xmlns':
                # Default namespace
                self.namespaces['default'] = attr_value
        
        # Also register namespaces with ElementTree for XPath queries
        for prefix, uri in self.namespaces.items():
            if prefix != 'default':
                ET.register_namespace(prefix, uri)
    
    def _parse_header(self, root: ET.Element) -> XTFHeader:
        """
        Parse the header section of an XTF file.
        
        Args:
            root: Root XML element
            
        Returns:
            XTFHeader with metadata
        """
        header = XTFHeader()

        def _local_name(elem: ET.Element) -> str:
            tag = elem.tag
            return tag.split('}')[-1] if '}' in tag else tag

        def _attr_ci(elem: ET.Element, key: str) -> Optional[str]:
            for k, v in elem.attrib.items():
                if k.lower() == key.lower():
                    return v
            return None

        # Find header section (namespaced or not, any case)
        header_elem = root.find('.//ili:headersection', self.namespaces)
        if header_elem is None:
            for elem in root.iter():
                if _local_name(elem).lower() == 'headersection':
                    header_elem = elem
                    break
        if header_elem is None:
            return header

        # Parse sender (attribute or element)
        sender_attr = _attr_ci(header_elem, 'SENDER')
        if sender_attr:
            header.sender = sender_attr.strip()
        else:
            sender_elem = header_elem.find('.//ili:sender', self.namespaces)
            if sender_elem is None:
                for elem in header_elem.iter():
                    if _local_name(elem).lower() == 'sender' and elem.text:
                        sender_elem = elem
                        break
            if sender_elem is not None and sender_elem.text:
                header.sender = sender_elem.text.strip()

        # Parse models (attribute NAME or text, namespaced or not)
        models_elem = header_elem.find('.//ili:models', self.namespaces)
        if models_elem is None:
            for elem in header_elem.iter():
                if _local_name(elem).lower() == 'models':
                    models_elem = elem
                    break
        if models_elem is not None:
            for model_elem in models_elem.iter():
                if _local_name(model_elem).lower() == 'model':
                    name_attr = _attr_ci(model_elem, 'NAME')
                    version_attr = _attr_ci(model_elem, 'VERSION')
                    uri_attr = _attr_ci(model_elem, 'URI')
                    name_text = model_elem.text.strip() if model_elem.text else None
                    model_name = (name_attr or name_text)
                    if model_name:
                        model_name = model_name.strip()
                        header.models.append(model_name)
                        header.model_refs.append(
                            XTFModelRef(
                                name=model_name,
                                version=version_attr.strip() if version_attr else None,
                                uri=uri_attr.strip() if uri_attr else None,
                            )
                        )

        # Parse optional comment
        comment_elem = header_elem.find('.//ili:comment', self.namespaces)
        if comment_elem is None:
            for elem in header_elem.iter():
                if _local_name(elem).lower() == 'comment' and elem.text:
                    comment_elem = elem
                    break
        if comment_elem is not None and comment_elem.text:
            header.comment = comment_elem.text.strip()

        # Fallback: infer model names from xmlns aliases on transfer root
        for attr_name, attr_value in root.attrib.items():
            ns_prefix = None
            if attr_name.startswith('{http://www.w3.org/2000/xmlns/}'):
                ns_prefix = attr_name.split('}')[1]
            elif attr_name.startswith('xmlns:'):
                ns_prefix = attr_name.split(':')[1]

            if not ns_prefix or ns_prefix in self.namespaces:
                # keep namespaces already captured; still use prefix as model alias
                pass

            if ns_prefix and ns_prefix not in header.models:
                # Heuristic: repository-style URIs used for model namespaces
                if "models.geo.admin.ch" in attr_value or "models.interlis.ch" in attr_value:
                    header.models.append(ns_prefix)
                    header.model_refs.append(
                        XTFModelRef(
                            name=ns_prefix,
                            uri=attr_value.strip() if attr_value else None,
                        )
                    )

        return header
    
    def _parse_baskets(self, root: ET.Element) -> List[XTFBasket]:
        """
        Parse all baskets from the data section.
        Supports both INTERLIS2.3 and INTERLIS2.4/xtf/2.4/INTERLIS namespaces.
        """
        baskets = []
        # Try all known data section tags
        datasection = None
        # Try with all known namespaces
        datasection_tags = [
            '{http://www.interlis.ch/INTERLIS2.3}DATASECTION',
            '{http://www.interlis.ch/INTERLIS2.4}DATASECTION',
            '{http://www.interlis.ch/xtf/2.4/INTERLIS}DATASECTION',
            'DATASECTION',
            'datasection',
        ]
        for tag in datasection_tags:
            datasection = root.find(f'.//{tag}')
            if datasection is not None:
                break
        if datasection is None:
            # Try lowercase for robustness
            for tag in datasection_tags:
                datasection = root.find(f'.//{tag.lower()}')
                if datasection is not None:
                    break
        if datasection is None:
            return baskets
        # Each direct child of datasection is a basket
        for basket_elem in datasection:
            basket = self._parse_basket(basket_elem)
            if basket:
                baskets.append(basket)
        return baskets
    
    def _parse_basket(self, basket_elem: ET.Element) -> Optional[XTFBasket]:
        """
        Parse a single basket element.
        
        Args:
            basket_elem: Basket XML element
            
        Returns:
            XTFBasket or None if invalid
        """
        # Get basket ID - try multiple approaches
        bid = None
        
        # Try with namespace
        if 'ili' in self.namespaces:
            bid = basket_elem.get(f'{{{self.namespaces["ili"]}}}bid')
            if not bid:
                bid = basket_elem.get(f'{{{self.namespaces["ili"]}}}BID')
        
        # Try without namespace (plain attribute)
        if not bid:
            bid = basket_elem.get('BID') or basket_elem.get('bid')
        
        # Try all known INTERLIS namespaces
        if not bid:
            interlis_namespaces = [
                'http://www.interlis.ch/INTERLIS2.3',
                'http://www.interlis.ch/INTERLIS2.4',
                'http://www.interlis.ch/xtf/2.4/INTERLIS',
            ]
            for ns in interlis_namespaces:
                bid = basket_elem.get(f'{{{ns}}}BID') or basket_elem.get(f'{{{ns}}}bid')
                if bid:
                    break
        
        if not bid:
            return None
        
        # Get topic name from tag (namespace:TopicName)
        tag = basket_elem.tag
        model_name = None
        if '}' in tag:
            ns_uri, local_name = tag[1:].split('}', 1)
            # Try to infer model name from namespace URI
            # Example: http://www.interlis.ch/xtf/2.4/DMAV_Bodenbedeckung_V1_0
            #          -> model name DMAV_Bodenbedeckung_V1_0
            if '/xtf/' in ns_uri:
                candidate = ns_uri.rstrip('/').split('/')[-1]
                if candidate not in ('INTERLIS', 'geometry', 'geom'):
                    model_name = candidate
            topic_name = f"{model_name}.{local_name}" if model_name else local_name
        else:
            topic_name = tag
        
        basket = XTFBasket(bid=bid, topic_name=topic_name)
        
        # Parse all objects in this basket
        for obj_elem in basket_elem:
            obj = self._parse_object(obj_elem, topic_name)
            if obj:
                basket.objects.append(obj)
        
        return basket
    
    def _parse_object(self, obj_elem: ET.Element, topic_name: str) -> Optional[XTFObject]:
        """
        Parse a single object element.
        
        Args:
            obj_elem: Object XML element
            topic_name: Name of the containing topic
            
        Returns:
            XTFObject or None if invalid
        """
        # Get TID (transfer ID) - try multiple approaches
        tid = None
        
        # Try with namespace
        if 'ili' in self.namespaces:
            tid = obj_elem.get(f'{{{self.namespaces["ili"]}}}tid')
            if not tid:
                tid = obj_elem.get(f'{{{self.namespaces["ili"]}}}TID')
        
        # Try without namespace (plain attribute)
        if not tid:
            tid = obj_elem.get('TID') or obj_elem.get('tid')
        
        # Try all known INTERLIS namespaces
        if not tid:
            interlis_namespaces = [
                'http://www.interlis.ch/INTERLIS2.3',
                'http://www.interlis.ch/INTERLIS2.4',
                'http://www.interlis.ch/xtf/2.4/INTERLIS',
            ]
            for ns in interlis_namespaces:
                tid = obj_elem.get(f'{{{ns}}}TID') or obj_elem.get(f'{{{ns}}}tid')
                if tid:
                    break
        
        if not tid:
            return None
        
        # Get class name from tag
        tag = obj_elem.tag
        if '}' in tag:
            class_name = tag.split('}')[1]
        else:
            class_name = tag
        
        obj = XTFObject(tid=tid, class_name=class_name)
        
        # Parse attributes and references
        for attr_elem in obj_elem:
            attr_name = attr_elem.tag
            if '}' in attr_name:
                attr_name = attr_name.split('}')[1]

            # Check if it's a direct reference (has ili:ref or REF attribute)
            ref = attr_elem.get(f'{{{self.namespaces["ili"]}}}ref')
            if not ref:
                ref = attr_elem.get('REF')

            if ref:
                obj.references[attr_name] = ref
            else:
                # Check for nested Reference structure (CatalogueObjectTrees pattern)
                # <Attribute><SomeRef><Reference REF="..."/></SomeRef></Attribute>
                ref_elem = None
                for child in attr_elem:
                    child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
                    if 'ref' in child_tag.lower():
                        # Found a Ref structure, look for nested Reference element
                        for grandchild in child:
                            grandchild_tag = grandchild.tag.split('}')[1] if '}' in grandchild.tag else grandchild.tag
                            if grandchild_tag.lower() == 'reference':
                                ref_value = grandchild.get('REF') or grandchild.get(f'{{{self.namespaces.get("ili", "")}}}ref')
                                if ref_value:
                                    obj.references[attr_name] = ref_value
                                    ref_elem = grandchild
                                    break
                        break

                # If no reference found, store as attribute value
                if attr_name not in obj.references:
                    # Try to convert COORD/POLYLINE to Shapely geometry
                    def is_coord(elem):
                        tag = elem.tag.split('}', 1)[-1] if '}' in elem.tag else elem.tag
                        return tag == 'COORD'
                    def is_polyline(elem):
                        tag = elem.tag.split('}', 1)[-1] if '}' in elem.tag else elem.tag
                        return tag == 'POLYLINE'

                    if len(attr_elem) > 0:
                        # COORD
                        if is_coord(attr_elem):
                            coords = []
                            for axis_elem in attr_elem:
                                if axis_elem.text and axis_elem.text.strip():
                                    coords.append(float(axis_elem.text.strip()))
                            if len(coords) >= 2:
                                obj.attributes[attr_name] = Point(coords)
                            else:
                                obj.attributes[attr_name] = attr_elem  # fallback
                        # POLYLINE
                        elif is_polyline(attr_elem):
                            # Find all COORD descendants (vertices)
                            points = []
                            for coord_elem in attr_elem.iter():
                                if is_coord(coord_elem):
                                    c = []
                                    for axis_elem in coord_elem:
                                        if axis_elem.text and axis_elem.text.strip():
                                            c.append(float(axis_elem.text.strip()))
                                    if len(c) >= 2:
                                        points.append(tuple(c))
                            if len(points) >= 2:
                                obj.attributes[attr_name] = LineString(points)
                            else:
                                obj.attributes[attr_name] = attr_elem  # fallback
                        else:
                            obj.attributes[attr_name] = attr_elem
                    elif attr_elem.text and attr_elem.text.strip():
                        obj.attributes[attr_name] = attr_elem.text.strip()

        # (Debug prints removed for normal operation)
        return obj
    
    def parse_catalog_file(self, catalog_path: str) -> Dict[str, XTFObject]:
        """
        Parse a catalog XML file and extract catalog items.
        
        Catalog files contain catalogue objects that can be referenced
        by XTF data files using REFERENCE attributes.
        
        Args:
            catalog_path: Path to the catalog XML file
            
        Returns:
            Dictionary mapping TID to XTFObject for all catalog items
        """
        catalog_items = {}
        try:
            tree = ET.parse(catalog_path)
            root = tree.getroot()
            self._update_namespaces(root)

            # Find data section - check multiple ways
            datasection = None
            for ns_key in ['ili', 'default']:
                if ns_key in self.namespaces:
                    ns = self.namespaces[ns_key]
                    datasection = root.find(f'{{{ns}}}DATASECTION')
                    if datasection is None:
                        datasection = root.find(f'.//{{{ns}}}DATASECTION')
                    if datasection is not None:
                        break
            if datasection is None:
                for elem in root:
                    tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
                    if tag.upper() == 'DATASECTION':
                        datasection = elem
                        break
            if datasection is None:
                print(f"No DATASECTION found in catalog file: {catalog_path}")
                return catalog_items

            # Parse all baskets in catalog
            for basket_elem in datasection:
                basket = self._parse_basket(basket_elem)
                if basket:
                    for obj in basket.objects:
                        catalog_items[obj.tid] = obj

            # Log catalog TID count for debugging
            print(f"Catalog file '{catalog_path}' loaded {len(catalog_items)} items: {list(catalog_items.keys())[:5]}...")

        except Exception as e:
            import sys
            print(f"Warning: Failed to parse catalog {catalog_path}: {e}", file=sys.stderr)

        return catalog_items


def parse_xtf(file_path: str) -> XTFDocument:
    """
    Convenience function to parse an XTF file.
    
    Args:
        file_path: Path to the .xtf file
        
    Returns:
        Parsed XTFDocument
        
    Example:
        >>> doc = parse_xtf("input/myModel.xtf")
        >>> print(f"Models: {doc.header.models}")
        >>> print(f"Baskets: {len(doc.baskets)}")
    """
    parser = XTFParser()
    return parser.parse_file(file_path)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        xtf_file = sys.argv[1]
        doc = parse_xtf(xtf_file)
        
        print(f"XTF File: {xtf_file}")
        print(f"Models: {', '.join(doc.header.models)}")
        print(f"Sender: {doc.header.sender}")
        print(f"Baskets: {len(doc.baskets)}")
        
        for basket in doc.baskets:
            print(f"\nBasket {basket.bid} ({basket.topic_name}):")
            print(f"  Objects: {len(basket.objects)}")
            for obj in basket.objects:
                print(f"    - {obj.class_name} (TID: {obj.tid})")
                for attr_name, attr_value in obj.attributes.items():
                    print(f"      {attr_name}: {attr_value}")
                for ref_name, ref_tid in obj.references.items():
                    print(f"      {ref_name} -> {ref_tid}")
    else:
        print("Usage: python xtf_parser.py <xtf_file>")
