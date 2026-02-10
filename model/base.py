"""
Constituants de base INTERLIS.

Ce module contient les éléments fondamentaux :
- MetaElement : classe de base abstraite pour tous les éléments du métamodèle
- ExtendableME : éléments extensibles (abstract, final, generic)
- Model, Topic : structure de base du modèle INTERLIS
- Documentation et traductions
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict

from model.dump import DumpMixin, Any


# ==========================================
# 2.1.1 Vue d'ensemble
# ==========================================

@dataclass
class IliDocumentation:
    """Documentation d'un élément INTERLIS (DocText)."""
    text: str
    language: str = "en"


# ==========================================
# 2.1.2 Classe MetaElement
# ==========================================

@dataclass
class MetaElement:
    """
    Classe de base abstraite pour tous les éléments de métamodèle.
    
    Un MetaElement est identifié par son nom (OID) et contient une documentation optionnelle.
    """
    name: str
    documentation: Optional[IliDocumentation] = None


# ==========================================
# 2.1.3 Gestion d'extensions
# ==========================================

@dataclass
class ExtendableME(MetaElement):
    """
    Élément de métamodèle extensible (Abstract, Final, Generic).
    
    Propriétés INTERLIS 2.4 :
    - abstract : indique une classe abstraite
    - final : classe ne peut pas être étendue
    - generic : classe générique avec paramètres
    """
    abstract: bool = False
    final: bool = False
    generic: bool = False  # INTERLIS 2.4


# ==========================================
# 2.1.4 Modèles et thèmes
# ==========================================

@dataclass
class Package(MetaElement):
    """Conteneur abstrait pour modèles et sous-modèles."""
    pass


@dataclass
class Model(MetaElement):
    """
    Modèle INTERLIS.
    
    Propriétés :
    - ili_version : version INTERLIS (ex: "2.4")
    - version : version du modèle (ex: "2022-10-10")
    - at : URL/URI du modèle
    - language : langue du modèle (ex: "en")
    - contracted : modèle contracté
    - kind : NormalM, TypeM, RefSystemM, SymbologyM
    """
    ili_version: str = "2.4"
    version: Optional[str] = None
    at: Optional[str] = None
    language: Optional[str] = None
    contracted: bool = False
    kind: str = "NormalM"
    charset: Optional[str] = None  # INTERLIS 2.4


@dataclass
class SubModel(Package):
    """Sous-modèle (Topic)."""
    pass


@dataclass
class Topic(MetaElement):
    """
    Thème INTERLIS (Topic).
    
    Conteneur de classes, domaines et associations.
    """
    ili_name: str = ""
    classes: Dict[str, Any] = field(default_factory=dict)
    domains: Dict[str, Any] = field(default_factory=dict)
    associations: Dict[str, Any] = field(default_factory=dict)


# ==========================================
# 2.1.5 Traductions
# ==========================================

@dataclass
class DocTextTranslation:
    """Traduction d'un texte de documentation."""
    text: str
    language: str = "en"


@dataclass
class METranslation:
    """Traduction d'un élément de métamodèle."""
    element: MetaElement  # Référence à l'élément traduit
    translated_name: Optional[str] = None
    translated_doc: List[DocTextTranslation] = field(default_factory=list)


@dataclass
class Translation(MetaElement):
    """
    Bloc de traductions pour un modèle.
    
    Contient les traductions de tous les éléments du modèle dans une langue donnée.
    """
    language: str = "en"
    translations: List[METranslation] = field(default_factory=list)
