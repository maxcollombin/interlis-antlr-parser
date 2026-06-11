"""
Package model : métamodèle INTERLIS canonique en Python.

Architecture pragmatique basée sur ce qui est réellement utilisé :
- base.py : Constituants de base (MetaElement, Model, Topic, Documentation)
- classes.py : Classes et attributs (Class, Attribute, Association, Role)
- views.py : Vues et graphiques (préparé pour extension future du parser)
- metamodel.py : IliModel, IliTopic, IliClass avec types de base
- resolver.py : Résolution sémantique après parsing
- serializer.py : Sérialisation JSON lisible
- ili_visitor.py : Visitor ANTLR pour construction AST

Les modules reflètent la couverture actuelle du parser ANTLR (~20% de IlisMeta16).
Extensions futures ajoutées quand la grammaire ANTLR les supporte.
"""

from model.metamodel import (
    # Base
    IliDocumentation,
    MetaElement,
    ExtendableME,
    Package,
    Model,
    SubModel,
    Topic,
    DocTextTranslation,
    METranslation,
    Translation,
    
    # Classes
    AttrOrParam,
    Attribute,
    Class,
    Structure,
    View,
    ReferenceType,
    Role,
    Association,
    Inheritance,
    DataUnit,
    Dependency,
    OIDType,
    
    # Types
    IliType,
    IliCardinality,
    IliGeometry,
    
    # Main model classes
    IliModel,
    IliTopic,
    IliDomain,
    IliAttribute,
    IliRole,
    IliAssociation,
    IliClass,
)

from model.resolver import IliResolver
from model.serializer import IliSerializer
from model.ili_visitor import IliVisitor

# Types et domaines
from model.types import (
    DomainType,
    TextType,
    NumericType,
    EnumerationType,
    EnumElement,
    BooleanType,
    DateTimeType,
    DateType,
    TimeType,
    AreaType,
    LengthType,
    AngleType,
    VertexType,
    SurfaceType,
    CoordType,
    LineType,
    BlackboxType,
    OIDDomainType,
    ClassType,
    FormattedType,
)

# Contraintes
from model.constraints import (
    Constraint,
    ConstraintSeverity,
    ConstraintScope,
    MandatoryConstraint,
    PlausibilityConstraint,
    ExistenceConstraint,
    UniqueConstraint,
    SetConstraint,
    CardinalityConstraint,
    AreaConnectedConstraint,
    LineTopologyConstraint,
    GeometryConstraint,
)

# Fonctions
from model.functions import (
    ArgumentKind,
    ReturnType,
    Argument,
    FunctionDeclaration,
    FunctionDefinition,
    FunctionCall,
    MethodCall,
    ProcedureDeclaration,
    ProcedureDefinition,
    BUILTIN_FUNCTIONS,
    lookup_builtin_function,
)

# Expressions (syntaxe et facteurs conceptuels)
from model.expressions import (
    Expression,
    Factor,
    PathFactor,
    ConstantFactor,
    UnitRefFactor,
    EnumMappingFactor,
    Literal,
)

# Dump (sérialisation lisible)
from model.dump import dump, DumpMixin

# Graphics (cartographie et symbologie)
from model.graphics import (
    ParameterType,
    LineStyle,
    FillPattern,
    Alignment,
    CartographicParameter,
    SymbologyReference,
    LineProperties,
    FillProperties,
    DrawingElement,
    SignParameterAssignment,
    TextProperties,
    GraphicElement,
    create_rgb_color,
)

# Views and Formations (section 2.5 et 2.6)
from model.views import (
    RenamedBaseView,
    ViewDefinition,
    Projection,
    JoinCondition,
    Join,
    Union,
    Formation,
    Graphic,
    SignParameter,
    ConditionalSignAssignment,
    DrawingRule,
    GraphicRule,
)

# Transfer formats and XTF (section 2.8)
from model.transfer import (
    TransferFormatType,
    OIDStrategy,
    CharacterSet,
    BasketTypeValue,
    TransferFormat,
    BasketDefinition,
    TransferEncoding,
    OIDGenerationStrategy,
    InterleaveRule,
    TransferConfiguration,
    DEFAULT_XTF_2_1,
    DEFAULT_XML_EXTENDED,
    DEFAULT_XML_RESTRICTED,
)

# XTF Parsing and Validation
from model.xtf_parser import (
    XTFHeader,
    XTFObject,
    XTFBasket,
    XTFDocument,
    XTFParser,
    parse_xtf,
)

from model.xtf_validator import (
    ValidationError,
    ValidationResult,
    XTFValidator,
    validate_xtf,
)

__all__ = [
    # Base
    "IliDocumentation",
    "MetaElement",
    "ExtendableME",
    "Package",
    "Model",
    "SubModel",
    "Topic",
    "DocTextTranslation",
    "METranslation",
    "Translation",
    
    # Classes
    "AttrOrParam",
    "Attribute",
    "Class",
    "Structure",
    "View",
    "ReferenceType",
    "Role",
    "Association",
    "Inheritance",
    "DataUnit",
    "Dependency",
    "OIDType",
    
    # Types
    "IliType",
    "IliCardinality",
    "IliGeometry",
    
    # Main model classes
    "IliModel",
    "IliTopic",
    "IliDomain",
    "IliAttribute",
    "IliRole",
    "IliAssociation",
    "IliClass",
    
    # Infrastructure
    "IliResolver",
    "IliSerializer",
    "IliVisitor",
    
    # Types et domaines
    "DomainType",
    "TextType",
    "NumericType",
    "EnumerationType",
    "EnumElement",
    "BooleanType",
    "DateTimeType",
    "DateType",
    "TimeType",
    "AreaType",
    "LengthType",
    "AngleType",
    "VertexType",
    "SurfaceType",
    "CoordType",
    "LineType",
    "BlackboxType",
    "OIDDomainType",
    "ClassType",
    "FormattedType",
    
    # Contraintes
    "Constraint",
    "ConstraintSeverity",
    "ConstraintScope",
    "MandatoryConstraint",
    "PlausibilityConstraint",
    "ExistenceConstraint",
    "UniqueConstraint",
    "SetConstraint",
    "CardinalityConstraint",
    "AreaConnectedConstraint",
    "LineTopologyConstraint",
    "GeometryConstraint",
    
    # Fonctions
    "ArgumentKind",
    "ReturnType",
    "Argument",
    "FunctionDeclaration",
    "FunctionDefinition",
    "FunctionCall",
    "MethodCall",
    "ProcedureDeclaration",
    "ProcedureDefinition",
    "BUILTIN_FUNCTIONS",
    "lookup_builtin_function",
    
    # Expressions (syntaxe et facteurs conceptuels)
    "Expression",
    "Factor",
    "PathFactor",
    "ConstantFactor",
    "UnitRefFactor",
    "EnumMappingFactor",
    "Literal",
    
    # Dump (sérialisation lisible)
    "dump",
    "DumpMixin",
    
    # Graphics (cartographie et symbologie)
    "ParameterType",
    "LineStyle",
    "FillPattern",
    "Alignment",
    "CartographicParameter",
    "SymbologyReference",
    "LineProperties",
    "FillProperties",
    "DrawingElement",
    "SignParameterAssignment",
    "TextProperties",
    "GraphicElement",
    "create_rgb_color",
    
    # Views and Formations
    "RenamedBaseView",
    "ViewDefinition",
    "Projection",
    "JoinCondition",
    "Join",
    "Union",
    "Formation",
    "Graphic",
    "SignParameter",
    "ConditionalSignAssignment",
    "DrawingRule",
    "GraphicRule",
    
    # Transfer formats
    "TransferFormatType",
    "OIDStrategy",
    "CharacterSet",
    "BasketTypeValue",
    "TransferFormat",
    "BasketDefinition",
    "TransferEncoding",
    "OIDGenerationStrategy",
    "InterleaveRule",
    "TransferConfiguration",
    "DEFAULT_XTF_2_1",
    "DEFAULT_XML_EXTENDED",
    "DEFAULT_XML_RESTRICTED",
    
    # XTF Parsing and Validation
    "XTFHeader",
    "XTFObject",
    "XTFBasket",
    "XTFDocument",
    "XTFParser",
    "parse_xtf",
    "ValidationError",
    "ValidationResult",
    "XTFValidator",
    "validate_xtf",
]
