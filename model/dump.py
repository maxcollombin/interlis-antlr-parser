"""
Dump INTERLIS : sérialisation lisible avec __repr__ et dump()

Fournit une représentation lisible du modèle INTERLIS sans JSON.
Chaque classe dataclass peut implémenter dump() pour une sortie personnalisée.
"""

from dataclasses import is_dataclass, fields
from typing import Any, List, Dict
from enum import Enum
from io import StringIO


def dump(obj: Any, indent: int = 0) -> str:
    """
    Génère une représentation lisible d'un objet INTERLIS.
    
    Utilise _dump_impl pour la sérialisation recursive.
    """
    return _dump_impl(obj, indent=indent)


def _dump_impl(obj: Any, indent: int = 0) -> str:
    """Implémentation récursive du dump."""
    prefix = "  " * indent
    
    if obj is None:
        return "None"
    
    if isinstance(obj, bool):
        return str(obj)
    
    if isinstance(obj, (int, float)):
        return str(obj)
    
    if isinstance(obj, str):
        return repr(obj)
    
    # Enums : afficher la valeur
    if isinstance(obj, Enum):
        return repr(obj.value)
    
    # Listes et tuples
    if isinstance(obj, (list, tuple)):
        if not obj:
            return "[]"
        
        items = []
        for item in obj:
            items.append(_dump_impl(item, indent=indent))
        
        if len(items) <= 1:
            return f"[{', '.join(items)}]"
        
        formatted_items = [f"{prefix}  {item}" for item in items]
        return "[\n" + ",\n".join(formatted_items) + f"\n{prefix}]"
    
    # Dictionnaires : afficher avec clés lisibles
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        
        items = []
        for key, value in obj.items():
            key_str = str(key) if not isinstance(key, str) else key
            dumped_value = _dump_impl(value, indent=indent + 1)
            
            # Si la valeur est multi-ligne, la mettre sur la ligne suivante
            if '\n' in dumped_value:
                items.append(f"{prefix}  {key_str}: {dumped_value}")
            else:
                items.append(f"{prefix}  {key_str}: {dumped_value}")
        
        return "{\n" + ",\n".join(items) + f"\n{prefix}}}"
    
    # Dataclasses
    if is_dataclass(obj):
        class_name = type(obj).__name__
        
        # Récupérer les champs pertinents (non privés, non None)
        relevant_fields = []
        for field in fields(obj):
            if field.name.startswith('_'):
                continue
            value = getattr(obj, field.name)
            if value is None or (isinstance(value, (list, dict)) and not value):
                continue
            relevant_fields.append((field.name, value))
        
        if not relevant_fields:
            return f"{class_name}()"
        
        items = []
        for field_name, field_value in relevant_fields:
            dumped_value = _dump_impl(field_value, indent=indent + 1)
            items.append(f"{prefix}  {field_name}={dumped_value}")
        
        return f"{class_name}(\n" + ",\n".join(items) + f"\n{prefix})"
    
    # Fallback
    return repr(obj)


class DumpMixin:
    """Mixin pour ajouter dump() et __repr__ aux dataclasses."""
    
    def dump(self, indent: int = 0) -> str:
        """Retourne une représentation lisible de l'objet."""
        return _dump_impl(self, indent=indent)
    
    def __repr__(self) -> str:
        """Représentation compact de l'objet."""
        class_name = type(self).__name__
        
        # Récupérer quelques champs clés pour le repr
        key_fields = []
        if hasattr(self, 'name') and self.name:
            key_fields.append(f"'{self.name}'")
        elif hasattr(self, 'ili_name') and self.ili_name:
            key_fields.append(f"'{self.ili_name}'")
        
        if key_fields:
            return f"{class_name}({key_fields[0]})"
        return f"{class_name}()"
