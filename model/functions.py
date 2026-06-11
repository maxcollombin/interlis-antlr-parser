"""
Fonctions et Procédures INTERLIS

Définitions et déclarations de fonctions et procédures définies dans IlisMeta16 section 2.5.
Classes pour représenter les fonctions, procédures, leurs arguments, types de retour et appels.

References: IlisMeta16 section 2.5
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, TYPE_CHECKING
from enum import Enum

from .base import MetaElement

if TYPE_CHECKING:
    from .expressions import Expression


# ==========================================
# Énumérations pour fonctions
# ==========================================

class ArgumentKind(Enum):
    """Type d'argument de fonction/procédure."""
    IN = "IN"          # Argument d'entrée (par défaut)
    OUT = "OUT"        # Argument de sortie
    INOUT = "INOUT"    # Argument d'entrée-sortie


class ReturnType(Enum):
    """Types de retour possibles pour les fonctions."""
    VOID = "VOID"                          # Pas de retour (procédures)
    TEXT = "TEXT"                          # Type texte
    NUMERIC = "NUMERIC"                    # Type numérique
    BOOLEAN = "BOOLEAN"                    # Type booléen
    DATETIME = "DATETIME"                  # Type date/heure
    ENUMERATION = "ENUMERATION"            # Type énumération
    STRUCTURE = "STRUCTURE"                # Type structure
    REFERENCE = "REFERENCE"                # Type référence
    DOMAIN = "DOMAIN"                      # Domaine personnalisé
    GEOMETRY = "GEOMETRY"                  # Type géométrique


# ==========================================
# Arguments de fonction/procédure
# ==========================================

@dataclass
class Argument:
    """
    Argument de fonction/procédure INTERLIS.
    
    Représente un paramètre formel avec son type et sa direction.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - name : nom de l'argument
    - type_name : nom du type (TEXT, NUMERIC, nom de domaine, etc.)
    - kind : IN, OUT, INOUT
    - cardinality : cardinalité (optionnelle pour collections)
    - mandatory : indique si l'argument est obligatoire
    """
    name: str
    type_name: Optional[str] = None
    kind: ArgumentKind = ArgumentKind.IN
    cardinality: Optional[str] = None  # e.g., "0..1", "1..*"
    mandatory: bool = False


# ==========================================
# Déclaration de fonction
# ==========================================

@dataclass
class FunctionDeclaration(MetaElement):
    """
    Déclaration de fonction INTERLIS (FUNCTION).
    
    Spécifie la signature d'une fonction sans implémentation.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - ili_name : nom complet de la fonction
    - arguments : liste des arguments formels
    - return_type : type de retour (ReturnType ou domaine personnalisé)
    - explanation : documentation/commentaire
    - is_builtin : indique si c'est une fonction intégrée
    """
    ili_name: str = ""
    arguments: List[Argument] = field(default_factory=list)
    return_type: Optional[str] = None
    explanation: Optional[str] = None
    is_builtin: bool = False


# ==========================================
# Définition de fonction (avec corps)
# ==========================================

@dataclass
class FunctionDefinition(FunctionDeclaration):
    """
    Définition de fonction INTERLIS avec implémentation.
    
    Complète la déclaration en ajoutant le corps de la fonction.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - body : corps de la fonction (facteur conceptuel / expression)
    """
    body: Optional['Expression'] = None


# ==========================================
# Déclaration de procédure
# ==========================================

@dataclass
class ProcedureDeclaration(MetaElement):
    """
    Déclaration de procédure INTERLIS (PROCEDURE).
    
    Similaire aux fonctions mais sans type de retour (return type = VOID).
    Souvent utilisée pour les actions avec effets de bord.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - ili_name : nom complet de la procédure
    - arguments : liste des arguments formels
    - explanation : documentation/commentaire
    - is_builtin : indique si c'est une procédure intégrée
    """
    ili_name: str = ""
    arguments: List[Argument] = field(default_factory=list)
    explanation: Optional[str] = None
    is_builtin: bool = False


# ==========================================
# Définition de procédure (avec corps)
# ==========================================

@dataclass
class ProcedureDefinition(ProcedureDeclaration):
    """
    Définition de procédure INTERLIS avec implémentation.
    
    Complète la déclaration de procédure en ajoutant le corps.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - body : corps de la procédure (facteur conceptuel / expression)
    """
    body: Optional['Expression'] = None


# ==========================================
# Appel de fonction/procédure (expression)
# ==========================================

@dataclass
class FunctionCall:
    """
    Appel de fonction INTERLIS dans une expression.
    
    Représente l'invocation d'une fonction avec ses arguments actuels.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - function_name : nom qualifié de la fonction appelée
    - arguments : liste des expressions d'arguments (facteurs conceptuels)
    """
    function_name: str
    arguments: List['Expression'] = field(default_factory=list)


@dataclass
class MethodCall:
    """
    Appel de méthode sur un objet INTERLIS.
    
    Représente un appel de fonction/procédure dans un contexte objet.
    
    References: IlisMeta16 section 2.5
    
    Propriétés :
    - object_ref : référence à l'objet (ex: "THIS", "Base")
    - method_name : nom de la méthode
    - arguments : liste des arguments actuels
    """
    object_ref: str  # e.g., "THIS", class reference
    method_name: str
    arguments: List['Expression'] = field(default_factory=list)


# ==========================================
# Registre des fonctions intégrées
# ==========================================

# Built-in functions registry (INTERLIS standard functions)
BUILTIN_FUNCTIONS: Dict[str, FunctionDeclaration] = {
    # Geometry functions
    "length": FunctionDeclaration(
        name="length",
        ili_name="INTERLIS.length",
        arguments=[Argument(name="lineform", type_name="LINEFORM", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the length of a lineform",
        is_builtin=True,
    ),
    "area": FunctionDeclaration(
        name="area",
        ili_name="INTERLIS.area",
        arguments=[Argument(name="surface", type_name="SURFACE", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the area of a surface",
        is_builtin=True,
    ),
    
    # String functions
    "strlen": FunctionDeclaration(
        name="strlen",
        ili_name="INTERLIS.strlen",
        arguments=[Argument(name="text", type_name="TEXT", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the length of a string",
        is_builtin=True,
    ),
    "substring": FunctionDeclaration(
        name="substring",
        ili_name="INTERLIS.substring",
        arguments=[
            Argument(name="text", type_name="TEXT", kind=ArgumentKind.IN),
            Argument(name="start", type_name="NUMERIC", kind=ArgumentKind.IN),
            Argument(name="length", type_name="NUMERIC", kind=ArgumentKind.IN),
        ],
        return_type="TEXT",
        explanation="Returns a substring",
        is_builtin=True,
    ),
    
    # Numeric functions
    "abs": FunctionDeclaration(
        name="abs",
        ili_name="INTERLIS.abs",
        arguments=[Argument(name="value", type_name="NUMERIC", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the absolute value",
        is_builtin=True,
    ),
    "sqrt": FunctionDeclaration(
        name="sqrt",
        ili_name="INTERLIS.sqrt",
        arguments=[Argument(name="value", type_name="NUMERIC", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the square root",
        is_builtin=True,
    ),
    "sin": FunctionDeclaration(
        name="sin",
        ili_name="INTERLIS.sin",
        arguments=[Argument(name="angle", type_name="NUMERIC", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the sine of an angle (in radians)",
        is_builtin=True,
    ),
    "cos": FunctionDeclaration(
        name="cos",
        ili_name="INTERLIS.cos",
        arguments=[Argument(name="angle", type_name="NUMERIC", kind=ArgumentKind.IN)],
        return_type="NUMERIC",
        explanation="Returns the cosine of an angle (in radians)",
        is_builtin=True,
    ),
    
    # Logical functions
    "defined": FunctionDeclaration(
        name="defined",
        ili_name="INTERLIS.defined",
        arguments=[Argument(name="value", type_name="DOMAIN", kind=ArgumentKind.IN)],
        return_type="BOOLEAN",
        explanation="Tests if a value is defined (not NULL)",
        is_builtin=True,
    ),
}

def lookup_builtin_function(name: str) -> Optional[FunctionDeclaration]:
    """
    Look up a built-in function by name.
    
    Args:
        name: Function name (case-sensitive)
    
    Returns:
        FunctionDeclaration if found, None otherwise
    """
    return BUILTIN_FUNCTIONS.get(name)
