"""
Vues et Formations INTERLIS (Views and Graphic)

Vues INTERLIS, formations et éléments graphiques.
Classes pour représenter les vues, formations et graphiques définis dans IlisMeta16 sections 2.5 et 2.6.

References: IlisMeta16 sections 2.5 (Views), 2.6 (Graphics)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, TYPE_CHECKING

from .base import MetaElement
from .classes import Class, Attribute

if TYPE_CHECKING:
    from .expressions import Expression


# ==========================================
# Section 2.5: Views et Formations
# ==========================================

@dataclass
class RenamedBaseView(MetaElement):
    """
    Base de vue renommée INTERLIS.
    
    Renomme une classe de vue de base pour la projection.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - base_view : classe de vue de base
    - new_name : nouveau nom pour la vue (optionnel)
    - or_null : indique si la vue peut être NULL
    """
    base_view: Optional[Class] = None
    new_name: Optional[str] = None
    or_null: bool = False


@dataclass
class ViewDefinition(MetaElement):
    """
    Définition de vue INTERLIS (VIEW).
    
    Vue simple combinant plusieurs classes de base avec renommage.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - views : liste des vues de base renommées
    """
    views: List[RenamedBaseView] = field(default_factory=list)


# ==========================================
# Formations: Projections, Joins, Unions
# ==========================================

@dataclass
class Projection(MetaElement):
    """
    Projection INTERLIS (field mapping dans une vue).
    
    Mappe un champ source vers un champ cible avec transformation optionnelle.
    
    References: IlisMeta16 section 2.5 (Formations / Projections)
    
    Propriétés :
    - source_field : Nom du champ source (chemin qualifié)
    - target_field : Nom du champ cible dans la vue
    - expression : Transformation optionnelle (facteur conceptuel)
    - renamed : Indique si le champ est simplement renommé
    """
    source_field: Optional[str] = None
    target_field: Optional[str] = None
    expression: Optional['Expression'] = None
    renamed: bool = False


@dataclass
class JoinCondition(MetaElement):
    """
    Condition de jointure INTERLIS.
    
    Définit comment lier deux classes dans un join.
    
    References: IlisMeta16 section 2.5 (Formations / Joins)
    
    Propriétés :
    - left_class : Classe/chemin gauche de la jointure
    - right_class : Classe/chemin droit de la jointure
    - on_expression : Expression de condition de join (facteur conceptuel)
    """
    left_class: Optional[str] = None
    right_class: Optional[str] = None
    on_expression: Optional['Expression'] = None


@dataclass
class Join(MetaElement):
    """
    Jointure INTERLIS (JOIN dans une formation).
    
    Combine plusieurs classes avec conditions de jointure.
    
    References: IlisMeta16 section 2.5 (Formations)
    
    Propriétés :
    - joins : Liste des conditions de jointure
    - join_type : Type de join (INNER, LEFT, RIGHT, FULL) - optionnel
    """
    joins: List[JoinCondition] = field(default_factory=list)
    join_type: Optional[str] = None  # INNER, LEFT, RIGHT, FULL


@dataclass
class Union(MetaElement):
    """
    Union INTERLIS (UNION dans une formation).
    
    Combine les résultats de plusieurs classes/formations.
    
    References: IlisMeta16 section 2.5 (Formations / Unions)
    
    Propriétés :
    - classes : Liste des classes/formations à unir
    - distinct : Éliminer les doublons
    """
    classes: List[str] = field(default_factory=list)
    distinct: bool = True


@dataclass
class Formation(MetaElement):
    """
    Formation INTERLIS (construction de vue complexe).
    
    Définit une vue complexe avec projections, joins et unions.
    
    References: IlisMeta16 section 2.5 (Formations)
    
    Propriétés :
    - ili_name : Nom complet de la formation
    - projections : Projections de champs
    - joins : Jointures entre classes
    - unions : Unions de résultats
    - where_clause : Clause de filtrage (facteur conceptuel)
    """
    ili_name: str = ""
    projections: List[Projection] = field(default_factory=list)
    joins: Optional[Join] = None
    unions: Optional[Union] = None
    where_clause: Optional['Expression'] = None


# ==========================================
# Section 2.6: Éléments graphiques
# ==========================================

@dataclass
class Graphic(MetaElement):
    """
    Élément graphique INTERLIS (GRAPHIC).
    
    Représentation graphique d'une classe avec conditions.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - ili_name : Nom complet du graphique
    - base_class : Classe base du graphique
    - where : Condition de restriction (facteur conceptuel)
    """
    ili_name: str = ""
    base_class: Optional[Class] = None
    where: Optional['Expression'] = None


@dataclass
class SignParameter:
    """
    Paramètre de symbole dans une règle de dessin.
    
    Représente un paramètre cartographique customisable.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - parameter : Attribut ou paramètre cartographique
    - assignment : Assignation de valeur (facteur conceptuel)
    """
    parameter: Optional[Attribute] = None
    assignment: Optional['Expression'] = None


@dataclass
class ConditionalSignAssignment(MetaElement):
    """
    Assignation conditionnelle de paramètres de symbole.
    
    Assigne les paramètres conditionnellement selon une expression.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - where : Condition d'application (facteur conceptuel)
    - parameters : Liste des assignations de paramètres
    """
    where: Optional['Expression'] = None
    parameters: List[SignParameter] = field(default_factory=list)


@dataclass
class DrawingRule(MetaElement):
    """
    Règle de dessin INTERLIS.
    
    Définit comment dessiner une classe avec assignations conditionnelles.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - ili_name : Nom complet de la règle
    - rules : Assignations conditionnelles
    - target_class : Classe cible de la règle
    - symbol : Symbole optionnel à utiliser
    """
    ili_name: str = ""
    rules: List[ConditionalSignAssignment] = field(default_factory=list)
    target_class: Optional[Class] = None
    symbol: Optional[str] = None  # Reference to symbol


@dataclass
class GraphicRule(MetaElement):
    """
    Règle graphique associant graphique et règles de dessin.
    
    Combine une définition graphique avec ses règles de dessin.
    
    References: IlisMeta16 section 2.6
    
    Propriétés :
    - graphic : Élément graphique
    - drawing_rules : Règles de dessin associées
    """
    graphic: Optional[Graphic] = None
    drawing_rules: List[DrawingRule] = field(default_factory=list)
