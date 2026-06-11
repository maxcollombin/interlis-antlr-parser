"""
Expressions INTERLIS (conceptuelles seulement)

Les éléments de syntaxe/grammaire restent dans le runtime ANTLR.
Ce module ne conserve que les nœuds conceptuels nécessaires pour porter
des références au modèle (attributs, constantes, unités, mappings d'énum).
"""

from pydantic import BaseModel
from typing import Optional


# ==========================================

# ==========================================
# Conceptual Expression Base (Pydantic)
# ==========================================

class Expression(BaseModel):
    """INTERLIS conceptual expression (no ANTLR syntax)."""
    pass

class Factor(Expression):
    """Base for factors (conceptual link to model)."""
    pass

class Literal(Expression):
    """Typed literal value."""
    value: str
    literal_type: str = "TEXT"

class PathFactor(Factor):
    """Reference to an attribute/path (e.g., THIS.Name, Base.Id)."""
    path: str

class ConstantFactor(Factor):
    """Constant factor (text, number, boolean)."""
    literal: Literal

class UnitRefFactor(Factor):
    """Unit reference (for derived/composite units only)."""
    unit_ref: str

class EnumMappingFactor(Factor):
    """Enumeration value mapping (notably for graphics)."""
    mapping: str
