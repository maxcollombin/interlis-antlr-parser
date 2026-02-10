"""
Fonctions INTERLIS

Définitions et déclarations de fonctions définies dans IlisMeta16 section 2.6.
Classes pour représenter les fonctions, leurs arguments et types de retour.

Note : Ces classes sont disponibles pour extension future du parser ANTLR.
Le visitor ne les instancie pas encore (enterFunctionDef non implémenté).
"""

from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING

from .base import MetaElement

if TYPE_CHECKING:
    from .expressions import Expression


# ==========================================
# Arguments de fonction
# ==========================================

@dataclass
class Argument:
    """
    Argument de fonction INTERLIS.
    
    Propriétés :
    - name : nom de l'argument
    - type_name : nom du type (TEXT, NUMERIC, nom de domaine, etc.)
    - kind : IN, OUT, INOUT
    """
    name: str
    type_name: Optional[str] = None
    kind: str = "IN"


# ==========================================
# Déclaration de fonction
# ==========================================

@dataclass
class FunctionDeclaration(MetaElement):
    """
    Déclaration de fonction INTERLIS (FUNCTION).
    
    Propriétés :
    - arguments : liste des arguments
    - return_type : type de retour
    - explanation : explication/commentaire
    """
    ili_name: str = ""
    arguments: List[Argument] = field(default_factory=list)
    return_type: Optional[str] = None
    explanation: Optional[str] = None


# ==========================================
# Définition de fonction (avec corps)
# ==========================================

@dataclass
class FunctionDefinition(FunctionDeclaration):
    """
    Définition de fonction INTERLIS avec corps.
    
    Propriétés :
    - body : corps de la fonction (facteur conceptuel)
    """
    body: Optional['Expression'] = None


# ==========================================
# Appel de fonction (expression)
# ==========================================

@dataclass
class FunctionCall:
    """
    Appel de fonction INTERLIS dans une expression.
    
    Propriétés :
    - function_name : nom de la fonction appelée
    - arguments : liste des expressions d'arguments (facteurs conceptuels)
    """
    function_name: str
    arguments: List['Expression'] = field(default_factory=list)
