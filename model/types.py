"""
Domaines et types INTERLIS

Domaines réutilisables et types de données définis dans IlisMeta16 section 2.3.
Classes pour représenter les domaines, types texte, numériques, énumérations, etc.

Note : Ces classes sont disponibles pour extension future du parser ANTLR.
Le visitor les instancie partiellement (enterDomainDef, enterEnumerationType).
"""

from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum

from .base import MetaElement


# ==========================================
# Domaines de base
# ==========================================

@dataclass
class DomainType(MetaElement):
    """
    Domaine INTERLIS (type de données réutilisable).
    
    Base pour tous les types de domaines : TextType, NumericType, EnumerationType, etc.
    """
    ili_name: str = ""
    mandatory: bool = False


# ==========================================
# Types textuels
# ==========================================

@dataclass
class TextType(DomainType):
    """
    Type textuel INTERLIS.
    
    Propriétés :
    - kind : TEXT, MTEXT (multiligne), URI, NAME
    - max_length : longueur maximale (optionnelle)
    """
    kind: str = "TEXT"
    max_length: Optional[int] = None


# ==========================================
# Types numériques
# ==========================================

@dataclass
class NumericType(DomainType):
    """
    Type numérique INTERLIS.
    
    Propriétés :
    - min_value : valeur minimale
    - max_value : valeur maximale
    - circular : intervalle circulaire
    - unit : unité de mesure
    """
    min_value: Optional[str] = None
    max_value: Optional[str] = None
    circular: bool = False
    unit: Optional[str] = None


# ==========================================
# Types énumération
# ==========================================

@dataclass
class EnumElement:
    """Élément d'une énumération (peut être hiérarchique)."""
    name: str
    sub_elements: List['EnumElement'] = field(default_factory=list)


@dataclass
class EnumerationType(DomainType):
    """
    Type énumération INTERLIS.
    
    Propriétés :
    - values : liste des valeurs possibles (hiérarchique)
    - final : énumération finale (non extensible)
    - ordered : énumération ordonnée
    """
    values: List[EnumElement] = field(default_factory=list)
    final: bool = False
    ordered: bool = False


# ==========================================
# Types booléens et dates
# ==========================================

@dataclass
class BooleanType(DomainType):
    """Type booléen INTERLIS."""
    kind: str = "BOOLEAN"


@dataclass
class DateTimeType(DomainType):
    """
    Type date/heure INTERLIS.
    
    Propriétés :
    - kind : FORMAT (date formatée), XMLDate, XMLTime, XMLDateTime
    """
    kind: str = "FORMAT"


# ==========================================
# Types de coordonnées et géométrie
# ==========================================

@dataclass
class CoordType(DomainType):
    """
    Type de coordonnées INTERLIS.
    
    Propriétés :
    - null_value : coordonnée NULL autorisée
    - multi_coord : multi-coordonnées
    - axes : liste des axes (x, y, z)
    """
    null_value: bool = False
    multi_coord: bool = False
    axes: List[str] = field(default_factory=list)


@dataclass
class LineType(DomainType):
    """
    Type ligne INTERLIS (POLYLINE, SURFACE, AREA).
    
    Propriétés :
    - kind : POLYLINE, SURFACE, AREA
    - with_straights : avec segments droits
    - with_arcs : avec arcs
    - coord_type : type de coordonnées
    """
    kind: str = "POLYLINE"
    with_straights: bool = True
    with_arcs: bool = False
    coord_type: Optional['CoordType'] = None


# ==========================================
# Autres types
# ==========================================

@dataclass
class BlackboxType(DomainType):
    """
    Type blackbox INTERLIS (données binaires).
    
    Propriétés :
    - kind : BINARY, XML
    """
    kind: str = "BINARY"


@dataclass
class OIDDomainType(DomainType):
    """
    Type OID INTERLIS (identifiant objet).
    
    Propriétés :
    - kind : TEXT, UUIDOID, I32OID, STANDARDOID, ANYOID
    """
    kind: str = "TEXT"


@dataclass
class ClassType(DomainType):
    """
    Type classe INTERLIS (référence à une classe).
    
    Propriétés :
    - ref_class : nom de la classe référencée
    - reference : type de référence (REFERENCE TO, RESTRICTION)
    """
    ref_class: Optional[str] = None
    reference: bool = False


@dataclass
class FormattedType(DomainType):
    """
    Type formaté INTERLIS.
    
    Propriétés :
    - format_string : chaîne de format
    - base_type : type de base (TEXT, NUMERIC, etc.)
    """
    format_string: Optional[str] = None
    base_type: Optional[DomainType] = None
