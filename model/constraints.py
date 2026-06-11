"""
Contraintes INTERLIS

Contraintes et règles de validation définies dans IlisMeta16 section 2.4.
Classes pour représenter les contraintes simples, d'existence, d'unicité, ensemblistes, etc.

References: IlisMeta16 sections 2.4 et 2.6
"""

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING, Union
from enum import Enum

from .base import MetaElement

try:
    from .expressions import Expression
except ImportError:
    Expression = None


# ==========================================
# Énumérations pour contraintes
# ==========================================

class ConstraintSeverity(Enum):
    """Niveau de sévérité d'une contrainte."""
    ERROR = "ERROR"      # Violation critique
    WARNING = "WARNING"  # Mise en garde
    INFO = "INFO"        # Information


class ConstraintScope(Enum):
    """À quel niveau s'applique la contrainte."""
    CLASS = "CLASS"            # Au niveau classe
    ATTRIBUTE = "ATTRIBUTE"    # Au niveau attribut
    ASSOCIATION = "ASSOCIATION"  # Au niveau association
    GLOBAL = "GLOBAL"          # Au modèle entier


# ==========================================
# Contraintes de base
# ==========================================

@dataclass
class Constraint(MetaElement):
    """
    Contrainte INTERLIS de base.
    
    Toutes les contraintes héritent de cette classe.
    Base pour tous les types de contraintes : Mandatory, Plausibility, etc.
    
    References: IlisMeta16 section 2.4
    
    Propriétés:
    - ili_name: Nom complet de la contrainte
    - applies_to: Élément concerné (classe, attribut, association)
    - severity: Niveau de sévérité (ERROR, WARNING, INFO)
    - scope: Portée de la contrainte
    """
    ili_name: str = ""
    applies_to: Optional[str] = None  # e.g., "MyModel.MyClass", "MyModel.MyClass.attribute"
    severity: ConstraintSeverity = ConstraintSeverity.ERROR
    scope: ConstraintScope = ConstraintScope.GLOBAL


# ==========================================
# Contraintes simples
# ==========================================

@dataclass
class MandatoryConstraint(Constraint):
    """
    Contrainte de valeur obligatoire (MANDATORY).
    
    Indique qu'un attribut ne peut pas être NULL.
    Propriétés :
    - attribute : attribut concerné
    - logical_expression : expression logique pour la contrainte
    
    References: IlisMeta16 section 2.4
    """
    attribute: Optional[str] = None
    logical_expression: Optional["Expression"] = None


@dataclass
class PlausibilityConstraint(Constraint):
    """
    Contrainte de plausibilité (CHECK, PERCENTAGE).
    
    Valide qu'une proportion d'objets satisfait une condition logique.
    
    Propriétés :
    - percentage : pourcentage de plausibilité (0-100)
    - direction : ALL (OBJECTS/CONSTRAINTS), >=, <=
    - logical_expression : expression logique (facteur conceptuel)
    
    References: IlisMeta16 section 2.4
    """
    percentage: Optional[float] = None
    direction: Optional[str] = None  # ALL, >=, <=
    logical_expression: Optional["Expression"] = None


# ==========================================
# Contraintes d'existence
# ==========================================

@dataclass
class ExistenceConstraint(Constraint):
    """
    Contrainte d'existence (EXISTENCE CONSTRAINT).
    
    Valide qu'une référence existe dans une autre classe.
    
    Propriétés :
    - attribute : attribut référencé
    - required_in : objet requis dans (classe cible)
    
    References: IlisMeta16 section 2.4
    """
    attribute: Optional[str] = None
    required_in: Optional[str] = None


# ==========================================
# Contraintes d'unicité
# ==========================================

@dataclass
class UniqueConstraint(Constraint):
    """
    Contrainte d'unicité (UNIQUE).
    
    Valide que certains attributs sont uniques parmi les objets.
    
    Propriétés :
    - where : condition de filtrage (optionnelle)
    - local : unicité locale (dans le dataset) ou globale
    - attributes : liste des attributs uniques
    
    References: IlisMeta16 section 2.4
    """
    where: Optional["Expression"] = None
    local: bool = False
    attributes: List[str] = field(default_factory=list)


# ==========================================
# Contraintes ensemblistes
# ==========================================

@dataclass
class SetConstraint(Constraint):
    """
    Contrainte ensembliste (SET CONSTRAINT).
    
    Exprime une contrainte sur un ensemble d'objets.
    
    Propriétés :
    - where : condition de filtrage (facteur conceptuel)
    - constraint_expression : expression de contrainte (facteur conceptuel)
    
    References: IlisMeta16 section 2.4
    """
    where: Optional["Expression"] = None
    constraint_expression: Optional["Expression"] = None


# ==========================================
# Contraintes de cardinalité
# ==========================================

@dataclass
class CardinalityConstraint(Constraint):
    """
    Contrainte de cardinalité sur les associations.
    
    Valide la cardinalité (1..*, 0..1, etc.) d'un rôle d'association.
    
    Propriétés :
    - min_cardinality : cardinalité minimale
    - max_cardinality : cardinalité maximale (None = *)
    - role : rôle concerné
    
    References: IlisMeta16 section 2.2
    """
    min_cardinality: Optional[int] = None
    max_cardinality: Optional[int] = None
    role: Optional[str] = None


# ==========================================
# Contraintes de géométrie
# ==========================================

@dataclass
class AreaConnectedConstraint(Constraint):
    """
    Contrainte topologique : l'aire doit être connexe (sans trous).
    
    Valide qu'une aire est topologiquement connexe.
    
    References: IlisMeta16 section 2.4, IlisMeta16 Appendix (Topology)
    """
    pass


@dataclass
class LineTopologyConstraint(Constraint):
    """
    Contrainte topologique pour lignes/polylignes.
    
    Valide les propriétés topologiques d'une ligne ou polyligne.
    
    Propriétés :
    - topology_rule : Règle de topologie (e.g., "NO_OVERLAPS", "NO_INTERSECTIONS")
    
    References: IlisMeta16 section 2.4, IlisMeta16 Appendix (Topology)
    """
    topology_rule: Optional[str] = None


@dataclass
class GeometryConstraint(Constraint):
    """
    Contrainte géométrique de base (abstraite).
    
    Base pour tous les types de contraintes géométriques.
    
    Propriétés :
    - geometry_type : Type de géométrie concernée (POINT, LINEFORM, SURFACE, AREA)
    
    References: IlisMeta16 section 2.4
    """
    geometry_type: Optional[str] = None
