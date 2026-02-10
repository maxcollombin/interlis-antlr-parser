"""
Contraintes INTERLIS

Contraintes et règles de validation définies dans IlisMeta16 section 2.6.
Classes pour représenter les contraintes simples, d'existence, d'unicité, ensemblistes, etc.

Note : Ces classes sont disponibles pour extension future du parser ANTLR.
Le visitor ne les instancie pas encore (enterConstraintDef non implémenté).
"""

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from .base import MetaElement

if TYPE_CHECKING:
    from .expressions import Expression


# ==========================================
# Contraintes de base
# ==========================================

@dataclass
class Constraint(MetaElement):
    """
    Contrainte INTERLIS de base.
    
    Toutes les contraintes héritent de cette classe.
    """
    ili_name: str = ""


# ==========================================
# Contraintes simples
# ==========================================

@dataclass
class MandatoryConstraint(Constraint):
    """
    Contrainte de valeur obligatoire (MANDATORY).
    
    Propriétés :
    - attribute : attribut concerné
    """
    attribute: Optional[str] = None


@dataclass
class PlausibilityConstraint(Constraint):
    """
    Contrainte de plausibilité (CHECK, PERCENTAGE).
    
    Propriétés :
    - percentage : pourcentage de plausibilité
    - direction : ALL (OBJECTS/CONSTRAINTS), >=, <=
    - logical_expression : expression logique (facteur conceptuel)
    """
    percentage: Optional[float] = None
    direction: Optional[str] = None  # ALL, >=, <=
    logical_expression: Optional['Expression'] = None


# ==========================================
# Contraintes d'existence
# ==========================================

@dataclass
class ExistenceConstraint(Constraint):
    """
    Contrainte d'existence (EXISTENCE CONSTRAINT).
    
    Propriétés :
    - attribute : attribut référencé
    - required_in : objet requis dans
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
    
    Propriétés :
    - where : condition de filtrage
    - local : unicité locale (dans le dataset)
    - attributes : liste des attributs uniques
    """
    where: Optional[str] = None
    local: bool = False
    attributes: List[str] = field(default_factory=list)


# ==========================================
# Contraintes ensemblistes
# ==========================================

@dataclass
class SetConstraint(Constraint):
    """
    Contrainte ensembliste (SET CONSTRAINT).
    
    Propriétés :
    - where : condition de filtrage (facteur conceptuel)
    - constraint_expression : expression de contrainte (facteur conceptuel)
    """
    where: Optional['Expression'] = None
    constraint_expression: Optional['Expression'] = None


# ==========================================
# Contraintes de cardinalité
# ==========================================

@dataclass
class CardinalityConstraint(Constraint):
    """
    Contrainte de cardinalité sur les associations.
    
    Propriétés :
    - min_cardinality : cardinalité minimale
    - max_cardinality : cardinalité maximale
    - role : rôle concerné
    """
    min_cardinality: Optional[int] = None
    max_cardinality: Optional[int] = None
    role: Optional[str] = None
