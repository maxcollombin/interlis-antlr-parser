"""
Classes et attributs INTERLIS.

Ce module contient les éléments pour définir des classes, attributs,
associations et rôles, correspondant à ce qui est extrait par le parser ANTLR.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from .base import MetaElement, ExtendableME
from model.dump import DumpMixin


# ==========================================
# 2.2.2 Structures et classes
# ==========================================

@dataclass
class AttrOrParam(ExtendableME):
    """
    Attribut ou paramètre INTERLIS.
    
    Propriétés :
    - abstract : attribut abstrait
    - final : attribut ne peut pas être redéfini
    - generic : paramètre générique
    - subdivision_kind : NoSubDiv, SubDiv, ContSubDiv
    - transient : attribut transitoire (pas de persistance)
    """
    ili_name: str = ""
    subdivision_kind: Optional[str] = None
    transient: bool = False
    derivates: List[str] = field(default_factory=list)


@dataclass
class Attribute(AttrOrParam):
    """Attribut d'une classe INTERLIS."""
    type_: str = "TEXT"
    mandatory: bool = False
    cardinality: Optional[str] = None
    geometry: Optional[str] = None

@dataclass
class Class(ExtendableME, DumpMixin):
    """
    Classe INTERLIS.
    
    Propriétés :
    - kind : Structure, Class, View, Association
    - attributes : attributs de la classe
    - base_class : classe de base (héritage)
    - multiplicity : pour associations
    """
    ili_name: str = ""
    kind: str = "Class"
    base_class: Optional['Class'] = None
    multiplicity: Optional[str] = None
    attributes: Dict[str, Attribute] = field(default_factory=dict)


@dataclass
class Structure(Class):
    """Structure INTERLIS (spécialisation de Class avec kind='Structure')."""
    kind: str = field(default="Structure", init=False)


@dataclass
class View(Class):
    """Vue INTERLIS (spécialisation de Class avec kind='View')."""
    kind: str = field(default="View", init=False)
    formation_kind: Optional[str] = None  # Projection, Join, Union, Aggregation, Inspection
    where: Optional[str] = None  # Condition de formation


# ==========================================
# 2.2.3 Relations et références
# ==========================================

@dataclass
class ReferenceType(ExtendableME):
    """Type de référence entre classes."""
    ili_name: str = ""
    external: bool = False
    base_class: Optional[Class] = None


@dataclass
class Role(ReferenceType):
    """
    Rôle dans une association INTERLIS.
    
    Propriétés :
    - name : nom du rôle
    - cardinality : cardinalité (ex: "0..1", "1..*")
    - strongness : Assoc, Aggr, Comp
    - ordered : rôle ordonné
    - multiplicity : multiplicité exacte
    """
    target_class: Optional[Class] = None
    strongness: str = "Assoc"
    ordered: bool = False
    multiplicity: Optional[str] = None
    embedded_transfer: bool = False


@dataclass
class Association(Class):
    """
    Association INTERLIS entre classes.
    
    kind = "Association"
    """
    kind: str = field(default="Association", init=False)
    role_a: Optional[Role] = None
    role_b: Optional[Role] = None


@dataclass
class Inheritance(MetaElement):
    """
    Relation d'héritage INTERLIS (EXTENDS).
    """
    sub_class: Optional[Class] = None
    super_class: Optional[Class] = None


# ==========================================
# 2.2.4 Unités de données
# ==========================================

@dataclass
class DataUnit(ExtendableME):
    """
    Unité de données (BASKET).
    
    Propriétés :
    - view_unit : unité de vue
    - dataunit_name : nom du panier
    """
    view_unit: bool = False
    dataunit_name: str = "BASKET"
    allowed_classes: List[Class] = field(default_factory=list)

@dataclass
class Dependency(MetaElement):
    """Dépendance entre unités de données."""
    using: Optional[DataUnit] = None
    dependent: Optional[DataUnit] = None


# ==========================================
# 2.2.5 OID quelconques
# ==========================================

@dataclass
class OIDType(MetaElement):
    """Type d'OID quelconque (AnyOIDType)."""
    ili_name: str = ""
    mandatory: bool = False
