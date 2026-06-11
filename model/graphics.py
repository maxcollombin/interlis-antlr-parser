"""
Éléments graphiques et cartographiques INTERLIS

Représentation graphique et cartographique des modèles INTERLIS.
Classes pour les symboles, règles de dessin, paramètres cartographiques.

References: IlisMeta16 section 2.6, Appendix (Symbology)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, TYPE_CHECKING
from enum import Enum

from .base import MetaElement

if TYPE_CHECKING:
    from .expressions import Expression


# ==========================================
# Énumérations pour paramètres cartographiques
# ==========================================

class ParameterType(Enum):
    """Type de paramètre cartographique."""
    NUMERIC = "NUMERIC"              # Valeur numérique
    STRING = "STRING"                # Chaîne de caractères
    COLOR = "COLOR"                  # Couleur RGB
    ENUMERATION = "ENUMERATION"      # Énumération
    BOOLEAN = "BOOLEAN"              # Booléen
    PATTERN = "PATTERN"              # Motif (ligne, remplissage)
    DIMENSION = "DIMENSION"          # Dimension (largeur, hauteur)


class LineStyle(Enum):
    """Style de ligne."""
    SOLID = "SOLID"                  # Ligne continue
    DASHED = "DASHED"                # Ligne pointillée
    DOTTED = "DOTTED"                # Ligne pointée
    DASH_DOT = "DASH_DOT"            # Trait-point


class FillPattern(Enum):
    """Motif de remplissage."""
    SOLID = "SOLID"                  # Remplissage uni
    HOLLOW = "HOLLOW"                # Sans remplissage
    HATCHED = "HATCHED"              # Hachures
    CROSS_HATCHED = "CROSS_HATCHED"  # Hachures croisées


class Alignment(Enum):
    """Alignement horizontal/vertical."""
    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"
    TOP = "TOP"
    MIDDLE = "MIDDLE"
    BOTTOM = "BOTTOM"


# ==========================================
# Paramètres cartographiques
# ==========================================

@dataclass
class CartographicParameter(MetaElement):
    """
    Paramètre cartographique INTERLIS.
    
    Représente un paramètre customisable dans un symbole ou une règle de dessin.
    Exemples: couleur, largeur de ligne, motif de remplissage.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - parameter_type : Type du paramètre (NUMERIC, STRING, COLOR, etc.)
    - default_value : Valeur par défaut (sérialisée en string)
    - min_value : Valeur minimale (pour paramètres numériques)
    - max_value : Valeur maximale (pour paramètres numériques)
    - enumeration_values : Valeurs possibles (pour énumérations)
    """
    parameter_type: ParameterType = ParameterType.NUMERIC
    default_value: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    enumeration_values: List[str] = field(default_factory=list)


# ==========================================
# Références de symbologie
# ==========================================

@dataclass
class SymbologyReference(MetaElement):
    """
    Référence à une symbologie externe INTERLIS.
    
    Pointe vers une symbologie définie dans une bibliothèque ou fichier externe.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - library_name : Nom de la bibliothèque (e.g., "StandardSymbology")
    - symbol_name : Nom du symbole dans la bibliothèque
    - version : Version de la symbologie (optionnelle)
    """
    library_name: str = ""
    symbol_name: Optional[str] = None
    version: Optional[str] = None


# ==========================================
# Propriétés de style
# ==========================================

@dataclass
class LineProperties(MetaElement):
    """
    Propriétés d'une ligne INTERLIS.
    
    Définit l'apparence d'une ligne (couleur, style, largeur).
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - color : Couleur en format RGB ou nommée (#RRGGBB ou "red")
    - width : Largeur de ligne en pixels ou points
    - style : Style de ligne (continu, pointillé, etc.)
    """
    color: Optional[str] = None  # "#RRGGBB" or "red"
    width: Optional[float] = None  # In pixels
    style: LineStyle = LineStyle.SOLID


@dataclass
class FillProperties(MetaElement):
    """
    Propriétés de remplissage INTERLIS.
    
    Définit l'apparence d'un remplissage (couleur, motif).
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - color : Couleur de remplissage
    - pattern : Motif de remplissage
    - background_color : Couleur de fond (pour motifs)
    """
    color: Optional[str] = None  # "#RRGGBB"
    pattern: FillPattern = FillPattern.SOLID
    background_color: Optional[str] = None


# ==========================================
# Éléments de dessin
# ==========================================

@dataclass
class DrawingElement(MetaElement):
    """
    Élément graphique à dessiner INTERLIS.
    
    Représente ce qu'il faut dessiner et comment (géométrie + style).
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - geometry_type : Type de géométrie (LINEFORM, POINT, SURFACE, AREA)
    - symbol : Référence à un symbole (alternative au style)
    - line_properties : Propriétés de ligne
    - fill_properties : Propriétés de remplissage
    - parameters : Paramètres cartographiques customisables
    """
    geometry_type: str = ""  # e.g., "LINEFORM", "POINT", "SURFACE", "AREA"
    symbol: Optional[SymbologyReference] = None
    line_properties: Optional[LineProperties] = None
    fill_properties: Optional[FillProperties] = None
    parameters: Dict[str, CartographicParameter] = field(default_factory=dict)


# ==========================================
# Assignations de paramètres
# ==========================================

@dataclass
class SignParameterAssignment(MetaElement):
    """
    Assignation concrète de valeur à un paramètre de symbole.
    
    Lie un paramètre cartographique à une valeur spécifique.
    Peut être conditionnelle.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - parameter : Le paramètre cartographique concerné
    - value : Valeur assignée
    - condition : Condition d'application (expression optionnelle)
    """
    parameter: Optional[CartographicParameter] = None
    value: Optional[str] = None
    condition: Optional['Expression'] = None  # Conditional assignment


# ==========================================
# Texte et alignement
# ==========================================

@dataclass
class TextProperties(MetaElement):
    """
    Propriétés de texte pour étiquettes INTERLIS.
    
    Définit comment afficher le texte (police, taille, couleur, alignement).
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - font_family : Famille de police (e.g., "Arial", "Helvetica")
    - font_size : Taille de police en points
    - color : Couleur du texte
    - bold : Gras
    - italic : Italique
    - horizontal_alignment : Alignement horizontal
    - vertical_alignment : Alignement vertical
    - background_color : Couleur du fond (optionnel)
    """
    font_family: Optional[str] = None
    font_size: Optional[float] = None
    color: Optional[str] = None
    bold: bool = False
    italic: bool = False
    horizontal_alignment: Alignment = Alignment.CENTER
    vertical_alignment: Alignment = Alignment.MIDDLE
    background_color: Optional[str] = None


# ==========================================
# Règles graphiques complètes
# ==========================================

@dataclass
class GraphicElement(MetaElement):
    """
    Élément graphique complet: géométrie + texte + style.
    
    Combine dessin et texte pour une représentation graphique complète.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - drawing_element : Élément de dessin (géométrie + style)
    - text_label : Étiquette textuelle optionnelle
    - text_properties : Propriétés du texte
    - orientation : Orientation en degrés (0-360)
    - layer : Couche de dessin (pour l'ordre de superposition)
    """
    drawing_element: Optional[DrawingElement] = None
    text_label: Optional[str] = None
    text_properties: Optional[TextProperties] = None
    orientation: Optional[float] = None  # 0-360 degrees
    layer: Optional[int] = None  # Drawing order


# ==========================================
# Utility functions
# ==========================================

def create_rgb_color(r: int, g: int, b: int) -> str:
    """
    Create an RGB color string.
    
    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
    
    Returns:
        Color string in format "#RRGGBB"
    """
    return f"#{r:02X}{g:02X}{b:02X}"
