"""
Métamodèle INTERLIS canonique en Python.

Architecture pragmatique basée sur ce qui est réellement utilisé par le parser ANTLR :
- base.py : Constituants de base (MetaElement, Model, Topic)
- classes.py : Classes et attributs (Class, Attribute)

Les modules sont créés en fonction de la couverture réelle du parser.
Extensions futures ajoutées quand la grammaire ANTLR les supporte.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional

from model.dump import DumpMixin
from enum import Enum

# ==========================================
# Imports depuis les modules de base
# ==========================================

# Constituants de base (MetaElement, Model, Topic)
from .base import (
    IliDocumentation,
    MetaElement,
    ExtendableME,
    Package,
    Model,
    SubModel,
    Topic,
    DocTextTranslation,
    METranslation,
    Translation,
)

# Classes et attributs
from .classes import (
    AttrOrParam,
    Attribute,
    Class,
    Structure,
    View,
    ReferenceType,
    Role,
    Association,
    Inheritance,
    DataUnit,
    Dependency,
    OIDType,
)

# Domaines / Types (IlisMeta 2.3)
from .types import DomainType


# ==========================================
# Types (simples, utilisés par le parser actuel)
# ==========================================

class IliType(Enum):
    """Énumération des types INTERLIS primitifs (utilisé par le visitor)."""
    TEXT = "TEXT"
    NUMERIC = "NUMERIC"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    ENUMERATION = "ENUMERATION"
    STRUCTURE = "STRUCTURE"
    BLACKBOX = "BLACKBOX"
    LINEFORM = "LINEFORM"
    COORDINATE = "COORDINATE"
    REFERENCE = "REFERENCE"
    OID = "OID"
    ANYOID = "ANYOID"


class IliCardinality:
    """Cardinalités INTERLIS."""
    ZeroToOne = "0..1"
    OneToOne = "1..1"
    ZeroToMany = "0..*"
    OneToMany = "1..*"


# ==========================================
# IliGeometry
# ==========================================

@dataclass
class IliGeometry:
    """Géométrie séparée du modèle (abstraction de type géométrique)."""
    name: str
    type_: str  # Exemple : "MULTIPOLYGON", "POINT", etc.
    dimensions: int = 2
    coordsys: Optional[str] = None  # Système de coordonnées


# ==========================================
# IliModel et IliTopic
# ==========================================

@dataclass
class IliModel(Model, DumpMixin):
    """
    Modèle INTERLIS avec structure complète.
    
    Hérite de Model pour les propriétés de base et ajoute la structure topologique.
    """
    # Structure
    topics: Dict[str, 'IliTopic'] = field(default_factory=dict)
    
    # Index pour accès rapide (construit par resolver)
    _classes_index: Dict[str, Class] = field(default_factory=dict, init=False, repr=False)
    _domains_index: Dict[str, 'IliDomain'] = field(default_factory=dict, init=False, repr=False)
    
    def resolve_class(self, ili_name: str) -> Optional[Class]:
        """Résout une classe par son nom INTERLIS complet."""
        return self._classes_index.get(ili_name)
    
    def resolve_domain(self, ili_name: str) -> Optional['IliDomain']:
        """Résout un domaine par son nom INTERLIS complet."""
        return self._domains_index.get(ili_name)


@dataclass
class IliTopic(Topic, DumpMixin):
    """
    Topic INTERLIS avec structure complète.
    
    Hérite de Topic et ajoute les types concrets.
    """
    classes: Dict[str, Class] = field(default_factory=dict)
    domains: Dict[str, 'IliDomain'] = field(default_factory=dict)
    associations: Dict[str, Association] = field(default_factory=dict)


# ==========================================
# IliDomain et IliAttribute pour compatibilité
# ==========================================

@dataclass
class IliDomain(DomainType):
    """
    Domaine INTERLIS (type de données réutilisable).
    
    Alias pour compatibilité avec le code existant.
    """
    ili_name: str = ""
    type_: IliType = IliType.TEXT
    mandatory: bool = False
    # enum_values, min_value, max_value, etc. sont dans les sous-classes spécialisées
    
    # Spécifiques à IliDomain
    enum_values: list = field(default_factory=list)
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    max_length: Optional[int] = None
    attributes: Dict[str, 'IliAttribute'] = field(default_factory=dict)  # Pour STRUCTURE


@dataclass
class IliAttribute(Attribute):
    """
    Attribut INTERLIS d'une classe ou structure.
    
    Alias pour compatibilité avec le code existant.
    """
    domain: Optional[IliDomain] = None  # Référence au domaine si applicable
    cardinality: str = IliCardinality.OneToOne
    geometry: Optional[IliGeometry] = None


@dataclass
class IliRole(Role):
    """
    Rôle dans une association INTERLIS.
    
    Alias pour compatibilité avec le code existant.
    """
    cardinality: str = IliCardinality.ZeroToOne


@dataclass
class IliAssociation(Association):
    """
    Association INTERLIS entre classes.
    
    Alias pour compatibilité avec le code existant.
    """
    pass


@dataclass
class IliClass(Class):
    """
    Classe INTERLIS.
    
    Alias pour compatibilité avec le code existant.
    """
    geometry: Optional[IliGeometry] = None


# ==========================================
# __all__ pour exports
# ==========================================

__all__ = [
    # 2.1 Basic
    "IliDocumentation",
    "MetaElement",
    "ExtendableME",
    "Package",
    "Model",
    "SubModel",
    "Topic",
    "DocTextTranslation",
    "METranslation",
    "Translation",
    
    # 2.2 Main
    "AttrOrParam",
    "Attribute",
    "Class",
    "Structure",
    "View",
    "ReferenceType",
    "Role",
    "Association",
    "Inheritance",
    "DataUnit",
    "Dependency",
    "OIDType",
    
    # Types
    "IliType",
    "IliCardinality",
    "IliGeometry",
    
    # Main model classes
    "IliModel",
    "IliTopic",
    "IliDomain",
    "IliAttribute",
    "IliRole",
    "IliAssociation",
    "IliClass",
]
