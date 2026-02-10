"""
Expressions INTERLIS (conceptuelles seulement)

Les éléments de syntaxe/grammaire restent dans le runtime ANTLR.
Ce module ne conserve que les nœuds conceptuels nécessaires pour porter
des références au modèle (attributs, constantes, unités, mappings d'énum).
"""

from dataclasses import dataclass
from typing import Optional


# ==========================================
# Base conceptuelle
# ==========================================

@dataclass
class Expression:
    """Expression INTERLIS conceptuelle (sans syntaxe ANTLR)."""
    pass


@dataclass
class Factor(Expression):
    """Base des facteurs (lien conceptuel vers le modèle)."""
    pass


@dataclass
class Literal(Expression):
    """Valeur littérale typée."""
    value: str
    literal_type: str = "TEXT"


@dataclass
class PathFactor(Factor):
    """Référence à un attribut/chemin (ex: THIS.Name, Base.Id)."""
    path: str


@dataclass
class ConstantFactor(Factor):
    """Facteur constant (texte, nombre, booléen)."""
    literal: Literal


@dataclass
class UnitRefFactor(Factor):
    """Référence d'unité (uniquement pour unités dérivées/composées)."""
    unit_ref: str


@dataclass
class EnumMappingFactor(Factor):
    """Projection de valeurs d'énumération (notamment pour le graphique)."""
    mapping: str
