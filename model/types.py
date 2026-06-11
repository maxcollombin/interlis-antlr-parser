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
    Supporte l'héritage de domaines via le champ 'extends'.
    
    References: IlisMeta16 section 2.3
    
    Propriétés:
    - ili_name: Nom complet du domaine (e.g., "MyModel.MyDomain")
    - mandatory: Indique si une valeur est obligatoire
    - extends: Domaine parent (pour TYPE ... EXTENDS ...)
    """
    ili_name: str = ""
    mandatory: bool = False
    extends: Optional['DomainType'] = None


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


# ==========================================
# Additional specialized types (Section 2.3)
# ==========================================

@dataclass
class DateType(DomainType):
    """
    Type DATE INTERLIS (date without time).
    
    Distinct from DateTimeType which includes time component.
    References: IlisMeta16 section 2.3
    """
    kind: str = "DATE"


@dataclass
class TimeType(DomainType):
    """
    Type TIMEOFDAY INTERLIS (time without date).
    
    Represents a time of day (hours, minutes, seconds).
    References: IlisMeta16 section 2.3
    """
    kind: str = "TIMEOFDAY"


@dataclass
class AreaType(DomainType):
    """
    Type AREA INTERLIS (surface area measurement domain).
    
    Represents area with units (m², km², ha, etc.).
    Circular: False (areas are not circular by definition)
    References: IlisMeta16 section 2.3
    
    Propriétés:
    - unit: Unité de surface (m2, km2, ha, etc.)
    """
    unit: Optional[str] = None  # e.g., "m2", "km2", "ha"


@dataclass
class LengthType(DomainType):
    """
    Type LENGTH INTERLIS (distance/length measurement domain).
    
    Represents linear measurement with units (m, km, cm, etc.).
    Circular: False (lengths are not circular)
    References: IlisMeta16 section 2.3
    
    Propriétés:
    - unit: Unité de longueur (m, km, cm, etc.)
    """
    unit: Optional[str] = None  # e.g., "m", "km", "cm"


@dataclass
class AngleType(DomainType):
    """
    Type ANGLE INTERLIS (angular measurement domain).
    
    Represents angular values with circular properties (0-360°).
    References: IlisMeta16 section 2.3
    
    Propriétés:
    - unit: DEGREES (défaut) ou RADIANS
    - min_value: Minimum angle (usually 0)
    - max_value: Maximum angle (usually 360 for degrees, 2π for radians)
    """
    unit: Optional[str] = "DEGREES"  # DEGREES or RADIANS
    min_value: Optional[float] = 0.0
    max_value: Optional[float] = 360.0


@dataclass
class VertexType(DomainType):
    """
    Type VERTEX INTERLIS (for polyline vertices).
    
    Represents a single vertex in a polyline or surface geometry.
    Each vertex has coordinate and may have properties.
    References: IlisMeta16 section 2.3
    
    Propriétés:
    - coord_type: Type de coordonnées pour ce vertex
    """
    coord_type: Optional['CoordType'] = None


@dataclass
class SurfaceType(DomainType):
    """
    Type SURFACE INTERLIS (surface geometry domain).
    
    Represents a closed surface with optional holes.
    References: IlisMeta16 section 2.3
    
    Propriétés:
    - with_holes: Indique si la surface peut avoir des trous
    """
    with_holes: bool = True
