"""
Serializer INTERLIS : sérialisation contrôlée en JSON/Dict.

Permet de limiter les attributs affichés et de rendre le JSON lisible.
"""

import json
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional
from model.metamodel import IliModel, IliTopic, IliClass, IliDomain


class IliSerializer:
    """Sérialise un modèle INTERLIS en JSON lisible."""
    
    # Attributs à inclure par défaut (whitelist)
    DEFAULT_MODEL_FIELDS = {"name", "ili_version", "topics", "contracted", "version", "language"}
    DEFAULT_TOPIC_FIELDS = {"name", "classes", "domains", "associations"}
    DEFAULT_CLASS_FIELDS = {"name", "abstract", "final", "attributes", "geometry", "kind"}
    DEFAULT_ATTRIBUTE_FIELDS = {"name", "type_", "mandatory", "geometry"}
    DEFAULT_DOMAIN_FIELDS = {"name", "type_", "enum_values", "min_value", "max_value"}
    DEFAULT_ASSOCIATION_FIELDS = {"name", "role_a", "role_b"}
    DEFAULT_ROLE_FIELDS = {"name", "cardinality", "target_class"}
    
    def __init__(self, include_documentation: bool = False, include_ili_names: bool = False):
        """
        Initialise le serializer.
        
        Args:
            include_documentation: Inclure les documentations
            include_ili_names: Inclure les noms INTERLIS complets
        """
        self.include_documentation = include_documentation
        self.include_ili_names = include_ili_names
    
    def to_dict(self, model: IliModel) -> Dict[str, Any]:
        """Convertit le modèle en dictionnaire (sans None, pas verbeux)."""
        return self._serialize_model(model)
    
    def to_json(self, model: IliModel, indent: int = 2) -> str:
        """Convertit le modèle en JSON formaté."""
        return json.dumps(self.to_dict(model), indent=indent, ensure_ascii=False, default=str)
    
    def _serialize_model(self, obj: IliModel) -> Dict[str, Any]:
        """Sérialise un IliModel."""
        result = {}
        
        # Ajouter version, at, language en premier
        if obj.version:
            result["version"] = obj.version
        if obj.at:
            result["at"] = obj.at
        if obj.language:
            result["language"] = obj.language
        
        # Puis les propriétés principales
        result["name"] = obj.name
        result["ili_version"] = obj.ili_version
        
        if obj.topics:
            result["topics"] = {
                name: self._serialize_topic(topic)
                for name, topic in obj.topics.items()
            }
        
        if obj.contracted:
            result["contracted"] = True
        
        if self.include_documentation and obj.documentation:
            result["documentation"] = obj.documentation.text
        
        return result
    
    def _serialize_topic(self, obj: IliTopic) -> Dict[str, Any]:
        """Sérialise un IliTopic."""
        result = {"name": obj.name}
        
        if obj.classes:
            result["classes"] = {
                name: self._serialize_class(cls)
                for name, cls in obj.classes.items()
            }
        
        if obj.domains:
            result["domains"] = {
                name: self._serialize_domain(domain)
                for name, domain in obj.domains.items()
            }
        
        if obj.associations:
            result["associations"] = {
                name: self._serialize_association(assoc)
                for name, assoc in obj.associations.items()
            }
        
        if self.include_documentation and obj.documentation:
            result["documentation"] = obj.documentation.text
        
        return result
    
    def _serialize_class(self, obj: IliClass) -> Dict[str, Any]:
        """Sérialise un IliClass."""
        result = {"name": obj.name}
        
        if obj.abstract:
            result["abstract"] = True
        if obj.final:
            result["final"] = True
        if obj.kind != "CLASS":
            result["kind"] = obj.kind
        
        if obj.attributes:
            result["attributes"] = {
                name: self._serialize_attribute(attr)
                for name, attr in obj.attributes.items()
            }
        
        if obj.geometry:
            result["geometry"] = self._serialize_geometry(obj.geometry)
        
        if self.include_documentation and obj.documentation:
            result["documentation"] = obj.documentation.text
        
        return result
    
    def _serialize_attribute(self, obj) -> Dict[str, Any]:
        """Sérialise un IliAttribute."""
        result = {
            "name": obj.name,
            "type": obj.type_.value if hasattr(obj.type_, 'value') else str(obj.type_),
        }
        
        if obj.mandatory:
            result["mandatory"] = True
        
        # Gérer cardinality qui peut être string ou enum
        cardinality_str = obj.cardinality.value if hasattr(obj.cardinality, 'value') else str(obj.cardinality)
        if cardinality_str != "1..1":
            result["cardinality"] = cardinality_str
        
        if obj.geometry:
            result["geometry"] = self._serialize_geometry(obj.geometry)
        
        if self.include_documentation and obj.documentation:
            result["documentation"] = obj.documentation.text
        
        return result
    
    def _serialize_domain(self, obj: IliDomain) -> Dict[str, Any]:
        """Sérialise un IliDomain."""
        result = {
            "name": obj.name,
            "type": obj.type_.value,
        }
        
        if obj.enum_values:
            result["enum_values"] = obj.enum_values
        if obj.min_value:
            result["min_value"] = obj.min_value
        if obj.max_value:
            result["max_value"] = obj.max_value
        if obj.max_length:
            result["max_length"] = obj.max_length
        if obj.mandatory:
            result["mandatory"] = True
        
        if obj.attributes:
            result["attributes"] = {
                name: self._serialize_attribute(attr)
                for name, attr in obj.attributes.items()
            }
        
        if self.include_documentation and obj.documentation:
            result["documentation"] = obj.documentation.text
        
        return result
    
    def _serialize_association(self, obj) -> Dict[str, Any]:
        """Sérialise une IliAssociation."""
        result = {
            "name": obj.name,
            "role_a": self._serialize_role(obj.role_a),
            "role_b": self._serialize_role(obj.role_b),
        }
        
        if self.include_documentation and obj.documentation:
            result["documentation"] = obj.documentation.text
        
        return result
    
    def _serialize_role(self, obj) -> Dict[str, Any]:
        """Sérialise un IliRole."""
        result = {"name": obj.name}
        
        if obj.cardinality.value != "0..1":
            result["cardinality"] = obj.cardinality.value
        
        if obj.target_class:
            result["target_class"] = obj.target_class.name if hasattr(obj.target_class, 'name') else str(obj.target_class)
        
        return result
    
    def _serialize_geometry(self, obj) -> Dict[str, Any]:
        """Sérialise un IliGeometry."""
        return {
            "name": obj.name,
            "type": obj.type_,
            "dimensions": obj.dimensions,
        }
