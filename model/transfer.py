"""
Format de Transfer INTERLIS (XTF et XML)

Modèles pour les configurations de transfert de données INTERLIS.
Classes pour les formats XTF, variantes XML, encodages, et stratégies d'OID.

References: IlisMeta16 section 2.8
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

from .base import MetaElement


# ==========================================
# Énumérations pour les formats
# ==========================================

class TransferFormatType(Enum):
    """Types de format de transfert supportés."""
    XTF = "XTF"              # eXtensible Transfer Format
    XTF_1 = "XTF_1"          # XTF Version 1.0
    XTF_2 = "XTF_2"          # XTF Version 2.0
    XTF_2_1 = "XTF_2_1"      # XTF Version 2.1
    XML = "XML"              # XML générique
    XML_RESTRICTED = "XML_RESTRICTED"  # XML restreint
    XML_EXTENDED = "XML_EXTENDED"      # XML étendu


class OIDStrategy(Enum):
    """Stratégies de génération d'OID dans le transfert."""
    BASELINE = "BASELINE"    # OID baseline (depuis première lecture)
    SEQUENTIAL = "SEQUENTIAL"  # OID séquentiels (0001, 0002, ...)
    UUID = "UUID"            # Identifiants UUID
    INTERLIS_OID = "INTERLIS_OID"  # OID INTERLIS standard
    I32 = "I32"              # Entiers 32-bit
    I64 = "I64"              # Entiers 64-bit


class CharacterSet(Enum):
    """Encodages de caractères supportés."""
    UTF8 = "UTF-8"           # Unicode UTF-8
    UTF16 = "UTF-16"         # Unicode UTF-16
    ISO_8859_1 = "ISO-8859-1"  # Latin-1
    ISO_8859_15 = "ISO-8859-15"  # Latin-9
    US_ASCII = "US-ASCII"    # ASCII américain
    CP1252 = "CP1252"        # Windows-1252


class BasketTypeValue(Enum):
    """Types de paniers de transfert."""
    MODEL = "MODEL"          # Panier de modèle
    TOPIC = "TOPIC"          # Panier de topic
    DATA = "DATA"            # Panier de données


# ==========================================
# Configuration de format de transfert
# ==========================================

@dataclass
class TransferFormat(MetaElement):
    """
    Configuration du format de transfert INTERLIS.
    
    Spécifie comment les données INTERLIS sont sérialisées et transmises.
    
    References: IlisMeta16 section 2.8
    
    Propriétés:
    - ili_name: Nom de la configuration de transfert
    - format_type: Type de format (XTF, XML, etc.)
    - version: Version du format (ex: "2.1" pour XTF 2.1)
    - encoding: Encodage de caractères utilisé
    - line_ending: Style de fin de ligne (LF, CR, CRLF)
    - include_metainfo: Inclure les métainformations dans le fichier
    - include_structure: Inclure la structure du modèle
    - basket_type: Type de panier utilisé par défaut
    - oid_strategy: Stratégie de génération d'OID
    - base_model: Modèle de base pour le transfert basé sur baseline
    """
    ili_name: str = ""
    format_type: TransferFormatType = TransferFormatType.XTF_2_1
    version: str = "2.1"
    encoding: CharacterSet = CharacterSet.UTF8
    line_ending: str = "LF"  # LF, CR, CRLF
    include_metainfo: bool = True
    include_structure: bool = False
    basket_type: BasketTypeValue = BasketTypeValue.DATA
    oid_strategy: OIDStrategy = OIDStrategy.BASELINE
    base_model: Optional[str] = None  # Model name for baseline


# ==========================================
# Définition de panier
# ==========================================

@dataclass
class BasketDefinition(MetaElement):
    """
    Définition d'un panier de transfert INTERLIS.
    
    Organise les données dans des conteneurs logiques pour le transfert.
    
    References: IlisMeta16 section 2.8
    
    Propriétés:
    - ili_name: Nom du panier
    - basket_type: Type de panier (MODEL, TOPIC, DATA)
    - topic_name: Nom du topic (pour paniers TOPIC)
    - model_name: Nom du modèle (pour paniers MODEL)
    - classes: Classes incluses dans le panier
    - object_count: Nombre d'objets dans le panier
    """
    ili_name: str = ""
    basket_type: BasketTypeValue = BasketTypeValue.DATA
    topic_name: Optional[str] = None
    model_name: Optional[str] = None
    classes: List[str] = field(default_factory=list)
    object_count: Optional[int] = None


# ==========================================
# Encodage et compression
# ==========================================

@dataclass
class TransferEncoding(MetaElement):
    """
    Spécifications d'encodage pour un transfert INTERLIS.
    
    Définit les paramètres d'encodage et de sérialisation.
    
    References: IlisMeta16 section 2.8
    
    Propriétés:
    - ili_name: Nom de l'encodage
    - charset: Ensemble de caractères
    - line_ending: Style de fin de ligne
    - compression: Type de compression (none, gzip, bzip2, etc.)
    - byte_order: Ordre des octets (little-endian, big-endian)
    - decimal_separator: Séparateur décimal ('.' ou ',')
    - attr_name_case: Casse des noms d'attributs (lower, upper, preserve)
    """
    ili_name: str = ""
    charset: CharacterSet = CharacterSet.UTF8
    line_ending: str = "LF"
    compression: str = "none"  # none, gzip, bzip2
    byte_order: str = "little-endian"
    decimal_separator: str = "."
    attr_name_case: str = "preserve"  # lower, upper, preserve


# ==========================================
# Configuration d'OID
# ==========================================

@dataclass
class OIDGenerationStrategy(MetaElement):
    """
    Stratégie de génération et assignation d'OID.
    
    Définit comment les OID sont générés et gérés dans le transfert.
    
    References: IlisMeta16 section 2.8
    
    Propriétés:
    - ili_name: Nom de la stratégie
    - strategy: Stratégie d'OID (BASELINE, SEQUENTIAL, UUID, etc.)
    - start_oid: Premier OID à générer (pour SEQUENTIAL)
    - oid_prefix: Préfixe d'OID (ex: "OBJ")
    - oid_width: Largeur minimum des OID numériques
    - preserve_external_oids: Conserver les OID externes
    - generate_missing: Générer OID pour objets sans OID
    """
    ili_name: str = ""
    strategy: OIDStrategy = OIDStrategy.BASELINE
    start_oid: Optional[int] = None
    oid_prefix: Optional[str] = None
    oid_width: int = 4  # Minimum width for numeric OIDs
    preserve_external_oids: bool = False
    generate_missing: bool = True


# ==========================================
# Règles d'entrelacement
# ==========================================

@dataclass
class InterleaveRule(MetaElement):
    """
    Règle d'entrelacement d'attributs dans le transfert.
    
    Définit l'ordre et le groupement des attributs lors de la sérialisation.
    
    References: IlisMeta16 section 2.8
    
    Propriétés:
    - ili_name: Nom de la règle
    - class_name: Classe concernée
    - interleave_type: Type d'entrelacement (SEQUENTIAL, GROUPED, BY_TYPE)
    - attributes: Ordre des attributs (liste)
    - depth_limit: Profondeur maximale d'entrelacement
    """
    ili_name: str = ""
    class_name: Optional[str] = None
    interleave_type: str = "SEQUENTIAL"  # SEQUENTIAL, GROUPED, BY_TYPE
    attributes: List[str] = field(default_factory=list)
    depth_limit: Optional[int] = None


# ==========================================
# Configuration de transfert complète
# ==========================================

@dataclass
class TransferConfiguration(MetaElement):
    """
    Configuration complète de transfert INTERLIS.
    
    Regroupe tous les paramètres nécessaires pour effectuer un transfert.
    
    References: IlisMeta16 section 2.8
    
    Propriétés:
    - ili_name: Nom de la configuration
    - transfer_format: Format de transfert
    - encoding: Configuration d'encodage
    - oid_strategy: Stratégie d'OID
    - baskets: Définitions de paniers
    - interleave_rules: Règles d'entrelacement
    - metadata: Métadonnées additionnelles
    - timestamp: Horodatage du transfert
    - source_model: Modèle source
    - target_models: Modèles cibles
    """
    ili_name: str = ""
    transfer_format: Optional[TransferFormat] = None
    encoding: Optional[TransferEncoding] = None
    oid_strategy: Optional[OIDGenerationStrategy] = None
    baskets: List[BasketDefinition] = field(default_factory=list)
    interleave_rules: List[InterleaveRule] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    timestamp: Optional[str] = None
    source_model: Optional[str] = None
    target_models: List[str] = field(default_factory=list)


# ==========================================
# Formats de transfert prédéfinis
# ==========================================

# Configuration standard XTF 2.1
DEFAULT_XTF_2_1 = TransferConfiguration(
    name="XTF_2_1_DEFAULT",
    ili_name="XTF_2_1_DEFAULT",
    transfer_format=TransferFormat(
        name="XTF_2_1_FORMAT",
        ili_name="XTF_2_1_FORMAT",
        format_type=TransferFormatType.XTF_2_1,
        version="2.1",
        encoding=CharacterSet.UTF8,
        oid_strategy=OIDStrategy.BASELINE,
    ),
    encoding=TransferEncoding(
        name="XTF_2_1_ENCODING",
        ili_name="XTF_2_1_ENCODING",
        charset=CharacterSet.UTF8,
        line_ending="LF",
        compression="none",
    ),
)

# Configuration XML étendue
DEFAULT_XML_EXTENDED = TransferConfiguration(
    name="XML_EXTENDED_DEFAULT",
    ili_name="XML_EXTENDED_DEFAULT",
    transfer_format=TransferFormat(
        name="XML_EXTENDED_FORMAT",
        ili_name="XML_EXTENDED_FORMAT",
        format_type=TransferFormatType.XML_EXTENDED,
        version="1.0",
        encoding=CharacterSet.UTF8,
        oid_strategy=OIDStrategy.UUID,
    ),
    encoding=TransferEncoding(
        name="XML_EXTENDED_ENCODING",
        ili_name="XML_EXTENDED_ENCODING",
        charset=CharacterSet.UTF8,
        line_ending="LF",
        compression="none",
    ),
)

# Configuration XML restreinte (plus compacte)
DEFAULT_XML_RESTRICTED = TransferConfiguration(
    name="XML_RESTRICTED_DEFAULT",
    ili_name="XML_RESTRICTED_DEFAULT",
    transfer_format=TransferFormat(
        name="XML_RESTRICTED_FORMAT",
        ili_name="XML_RESTRICTED_FORMAT",
        format_type=TransferFormatType.XML_RESTRICTED,
        version="1.0",
        encoding=CharacterSet.UTF8,
        include_metainfo=False,
        oid_strategy=OIDStrategy.SEQUENTIAL,
    ),
    encoding=TransferEncoding(
        name="XML_RESTRICTED_ENCODING",
        ili_name="XML_RESTRICTED_ENCODING",
        charset=CharacterSet.UTF8,
        line_ending="LF",
        compression="gzip",
    ),
)
