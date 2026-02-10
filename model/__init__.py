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
    MandatoryConstraint,
    PlausibilityConstraint,
    ExistenceConstraint,
    UniqueConstraint,
    SetConstraint,
    CardinalityConstraint,
)

# Fonctions
from model.functions import (
    Argument,
    FunctionDeclaration,
    FunctionDefinition,
    FunctionCall,
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

# Views (préparé pour extension future)
from model.views import (
    RenamedBaseView,
    ViewDefinition,
    Graphic,
    SignParameter,
    ConditionalSignAssignment,
    DrawingRule,
    GraphicRule,
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
    "CoordType",
    "LineType",
    "BlackboxType",
    "OIDDomainType",
    "ClassType",
    "FormattedType",
    
    # Contraintes
    "Constraint",
    "MandatoryConstraint",
    "PlausibilityConstraint",
    "ExistenceConstraint",
    "UniqueConstraint",
    "SetConstraint",
    "CardinalityConstraint",
    
    # Fonctions
    "Argument",
    "FunctionDeclaration",
    "FunctionDefinition",
    "FunctionCall",
    
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
    
    # Views (préparé pour extension future)
    "RenamedBaseView",
    "ViewDefinition",
    "Graphic",
    "SignParameter",
    "ConditionalSignAssignment",
    "DrawingRule",
    "GraphicRule",
]
