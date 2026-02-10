"""
Vues et graphique (Views and Graphic)

Vues INTERLIS et éléments graphiques (symboles, règles de dessin).
Classes pour représenter les vues et graphiques définis dans IlisMeta16 section 2.5.

Note : Ces classes sont disponibles pour extension future du parser ANTLR.
Actuellement, le visitor ne les instancie pas encore (enterViewDef non implémenté).
"""

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from .base import MetaElement
from .classes import Class, Attribute

if TYPE_CHECKING:
    from .expressions import Expression


# ==========================================
# 2.5.1 Vues
# ==========================================

@dataclass
class RenamedBaseView(MetaElement):
    """
    Base de vue renommée.
    
    Propriétés :
    - base_view : classe de vue de base
    - or_null : peut être NULL
    """
    base_view: Optional[Class] = None
    or_null: bool = False


@dataclass
class ViewDefinition(MetaElement):
    """
    Définition de vue INTERLIS.
    
    Propriétés :
    - views : vues de base renommées
    """
    views: List[RenamedBaseView] = field(default_factory=list)


# ==========================================
# 2.5.2 Éléments graphiques
# ==========================================

@dataclass
class Graphic(MetaElement):
    """
    Élément graphique INTERLIS.
    
    Propriétés :
    - base_class : classe de base
    - where : condition de restriction graphique (facteur conceptuel)
    """
    ili_name: str = ""
    base_class: Optional[Class] = None
    where: Optional['Expression'] = None


@dataclass
class SignParameter:
    """Paramètre de symbole dans une règle de dessin."""
    parameter: Optional[Attribute] = None
    assignment: Optional['Expression'] = None


@dataclass
class ConditionalSignAssignment(MetaElement):
    """
    Assignation conditionnelle de paramètres de symbole.
    
    Propriétés :
    - where : condition (facteur conceptuel)
    - parameters : assignations de paramètres
    """
    where: Optional['Expression'] = None
    parameters: List[SignParameter] = field(default_factory=list)


@dataclass
class DrawingRule(MetaElement):
    """
    Règle de dessin INTERLIS.
    
    Propriétés :
    - rules : assignations conditionnelles
    """
    ili_name: str = ""
    rules: List[ConditionalSignAssignment] = field(default_factory=list)
    target_class: Optional[Class] = None


@dataclass
class GraphicRule(MetaElement):
    """
    Règle graphique associant graphique et règles de dessin.
    """
    graphic: Optional[Graphic] = None
    drawing_rules: List[DrawingRule] = field(default_factory=list)
