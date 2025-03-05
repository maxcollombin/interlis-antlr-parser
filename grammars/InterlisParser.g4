parser grammar InterlisParser;
options { tokenVocab=InterlisLexer; }

// Règle principale

interlis2def : INTERLIS WS Dec SEMI { modeldef };

// Définition du modèle

modeldef : CONTRACTED? (TYPE | REFSYSTEM | SYMBOLOGY)?
           MODEL Name (LPAR Name RPAR)?
           AT STRING
           VERSION STRING Explanation?
           (TRANSLATION OF Name LSBR STRING RSBR)? EQ
           (IMPORTS UNQUALIFIED? Name (COMMA UNQUALIFIED? Name)* SEMI)*
           (MetaDataBasketDef
           | UnitDef
           | FunctionDef
           | LineFormTypeDef
           | DomainDef
           | RunTimeParameterDef
           | ClassDef
           | StructureDef
           | topicDef)*
           END Name DOT;

// Thèmes

topicDef : VIEW? TOPIC Name
           PropertyKeyword? (ABSTRACT | FINAL)?
           (EXTENDS Name)? EQ
           (BASKET OID AS Name SEMI)?
           (OID AS Name SEMI)?
           (DEPENDS ON Name (COMMA Name)* SEMI)?
           (MetaDataBasketDef
           | UnitDef
           | FunctionDef
           | LineFormTypeDef
           | DomainDef
           | RunTimeParameterDef
           | ClassDef
           | StructureDef
           | topicDef)*
           END Name SEMI;

Definitions : MetaDataBasketDef
            | UnitDef
            | FunctionDef
            | DomainDef
            | ClassDef
            | StructureDef
            | AssociationDef
            | ConstraintsDef
            | ViewDef
            | GraphicDef;

TopicRef : (Name DOT)? Name;

// Classes et structures

ClassDef : CLASS Name
             PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
               (EXTENDS ClassOrStructureRef)? EQ
               ((OID AS Name | NO OID) SEMI)?
             ClassOrStructureDef
           END Name SEMI;

StructureDef : STRUCTURE Name
                 PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
                   (EXTENDS StructureRef)? EQ
                 ClassOrStructureDef
               END Name SEMI;

ClassRef : (Name DOT (Name DOT)?)? Name;
ClassOrStructureDef : (ATTRIBUTE AttributeDef+ | ConstraintDef+ | PARAMETER ParameterDef+)+;

StructureRef : (Name DOT (Name DOT)?)? Name;

ClassOrStructureRef : ClassRef | StructureRef;

// Attributs

AttributeDef : CONTINUOUS? SUBDIVISION?
               Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
               COLON AttrTypeDef
               (COLON EQ factor (COMMA factor)*)? SEMI;

AttrTypeDef : MANDATORY? AttrType
            | (BAG | LIST) Cardinality? OF RestrictedStructureRef;

AttrType : Type
         | DomainRef
         | ReferenceAttr
         | RestrictedStructureRef;

ReferenceAttr : REFERENCE TO PropertyKeyword? EXTERNAL? RestrictedClassOrAssRef;

RestrictedClassOrAssRef : (ClassOrAssociationRef | ANYCLASS)
                        (RESTRICTION LPAR ClassOrAssociationRef (COMMA ClassOrAssociationRef)* RPAR)?;

ClassOrAssociationRef : ClassRef | AssociationRef;

RestrictedStructureRef : (StructureRef | ANYSTRUCTURE)
                       (RESTRICTION LPAR StructureRef (COMMA StructureRef)* RPAR)?;

RestrictedClassOrStructureRef : (ClassOrStructureRef | ANYSTRUCTURE)
                              (RESTRICTION LPAR ClassOrStructureRef (COMMA ClassOrStructureRef)* RPAR)?;

// Relations vraies / Associations

AssociationDef : ASSOCIATION Name
                     PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | OID)?
                     (EXTENDS AssociationRef)?
                     (DERIVED FROM Name)? EQ
                     ((OID AS Name | NO OID) SEMI)?
                     RoleDef*
                     (ATTRIBUTE AttributeDef*)?
                     (CARDINALITY EQ Cardinality SEMI)?
                     ConstraintDef*
                 END Name SEMI;

AssociationRef : (Name DOT (Name DOT)?)? Name;

RoleDef : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | HIDING | ORDERED | EXTERNAL)?
              (MINUS MINUS | MINUS LT GT | MINUS LT HASH GT) Cardinality?
              RestrictedClassOrAssRef (OR RestrictedClassOrAssRef)*
              (COLON EQ STRING)? SEMI;

Cardinality : LCBR (MUL | PosNumber (DOT DOT (PosNumber | MUL))?) RCBR;

// Domaines de valeurs et constantes

DomainDef : DOMAIN Name PropertyKeyword? (ABSTRACT | FINAL)?
                (EXTENDS DomainRef)? EQ
                (MANDATORY? Type | Type) SEMI;

Type : BaseType | LineType;

DomainRef : (Name DOT (Name DOT)?)? Name;

BaseType : TextType
           | EnumerationType
           | EnumTreeValueType
           | AlignmentType
           | BooleanType
           | NumericType
           | FormattedType
           | CoordinateType
           | OIDType
           | BlackboxType
           | ClassType
           | AttributeType;

Constant : UNDEFINED
         | NumericConst
         | TextConst
         | FormattedConst
         | EnumerationConst
         | ClassConst
         | AttributePathConst;

// Chaînes de caractères

TextType : MTEXT (MUL PosNumber)?
         | TEXT (MUL PosNumber)?
         | NAME
         | URI;

TextConst : STRING;

// Enumérations

EnumerationType : ENUM LCBR EnumElement (COMMA EnumElement)* RCBR (ORDERED | CIRCULAR)?;

EnumTreeValueType : ALL OF DomainRef;

Enumeration : LPAR EnumElement (COMMA EnumElement)* (COLON FINAL)? RPAR;

EnumElement : Name (DOT Name)* (Enumeration)?;

EnumerationConst : HASH (Name (DOT Name)* (DOT OTHERS)? | OTHERS);

// Alignement du texte

AlignmentType : ( HALIGNMENT | VALIGNMENT );

// Boolean

BooleanType : BOOLEAN;

// Types de données numériques

NumericType : (Dec DOT DOT Dec | NUMERIC) CIRCULAR?
        (LSBR UnitRef RSBR)?
        (CLOCKWISE | COUNTERCLOCKWISE | RefSys)?;

RefSys : LCBR MetaObjectRef (LSBR PosNumber RSBR)? RCBR
     | LT DomainRef (LSBR PosNumber RSBR)? GT;

DecConst : Dec | PI | LNBASE;

NumericConst : DecConst (LSBR UnitRef RSBR)?;

// Domaines de valeurs formatés

FormattedType : FORMAT BASED ON StructureRef FormatDef
        | FORMAT DomainRef STRING DOT DOT STRING;

FormatDef : LPAR INHERITANCE? STRING? (BaseAttrRef STRING)* BaseAttrRef STRING? RPAR;

BaseAttrRef : Name (DIV PosNumber)?
      | Name DIV DomainRef;

FormattedConst : STRING;

// Date et heure

DateTimeType : ( DATE | TIMEOFDAY | DATETIME );

// Coordonnées

CoordinateType : COORD NumericType
           (COMMA NumericType (COMMA NumericType)?
             (COMMA RotationDef)?)?;

RotationDef : ROTATION NullAxisPosNumber MINUS GT PiHalfAxisPosNumber;

NullAxisPosNumber : PosNumber;
PiHalfAxisPosNumber : PosNumber;

ContextDef : CONTEXT Name EQ LCBR DomainRef EQ DomainRef (OR DomainRef)* SEMI RCBR SEMI;

// Domaines de valeurs des identifications d’objet

OIDType : OID ( ANY | NumericType | TextType );

// Boîtes noires

BlackboxType : BLACKBOX ( XML | BINARY );

// Domaines de valeurs de classes et chemins d’attributs

ClassType : CLASS
        (RESTRICTION LPAR ViewableRef (COMMA ViewableRef)* RPAR)?
      | STRUCTURE
        (RESTRICTION LPAR ClassOrStructureRef (COMMA ClassOrStructureRef)* RPAR)?;

AttributeType : ATTRIBUTE
          (OF (ClassType DOT AttributePath | AT_SYMBOL Name))?
          (RESTRICTION LPAR AttrTypeDef (COMMA AttrTypeDef)* RPAR)?;

ClassConst : GT ViewableRef;

AttributePathConst : GT GT (ViewableRef DOT)? Name;

// Polylignes

LineType : ( DIRECTED? POLYLINE | SURFACE | AREA | DIRECTED? MULTIPOLYLINE | MULTISURFACE | MULTIAREA )
        LineForm? ControlPoints? IntersectionDef?;

LineForm : WITH LPAR LineFormType { COMMA LineFormType } RPAR;

LineFormType : STRAIGHTS | ARCS | Name DOT Name;

ControlPoints : VERTEX Name;

IntersectionDef : WITHOUT OVERLAPS GT Dec;

LineFormTypeDef : LINE FORM LCBR Name COLON Name SEMI RCBR;

// Unités composées

UnitDef : UNIT Name
      (LPAR ABSTRACT RPAR)?
      (LSBR Name RSBR)?
      (EXTENDS UnitRef)?
      (EQ (DerivedUnit | ComposedUnit))? SEMI;

DerivedUnit : (DecConst ((MUL | DIV) DecConst)*
        | FUNCTION Explanation) LSBR UnitRef RSBR;

ComposedUnit : LPAR UnitRef ((MUL | DIV) UnitRef)* RPAR;

UnitRef : (Name DOT (Name DOT)?)? Name;

// Traitement des méta-objets

MetaDataBasketDef : SIGN | REFSYSTEM BASKET Name
           PropertyKeyword? FINAL?
           (EXTENDS MetaDataBasketRef)?
           TILDE TopicRef
           (OBJECTS OF Name COLON Name (COMMA Name)*)? SEMI;

MetaDataBasketRef : (Name DOT (Name DOT)?)? Name;

MetaObjectRef : (MetaDataBasketRef DOT)? Name;

// Paramètres

ParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
         COLON (AttrTypeDef | METAOBJECT (OF MetaObjectRef)?) SEMI;

// Paramètres d’exécution

RunTimeParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
            COLON AttrTypeDef SEMI;

// Conditions de cohérence

ConstraintDef : MandatoryConstraint
        | PlausibilityConstraint
        | ExistenceConstraint
        | UniquenessConstraint
        | SetConstraint;

MandatoryConstraint : MANDATORY CONSTRAINT Expression SEMI;

PlausibilityConstraint : CONSTRAINT
             ( LTEQ | GTEQ ) Dec MOD
             Expression SEMI;

ExistenceConstraint : EXISTENCE CONSTRAINT
           AttributePath REQUIRED IN
           ViewableRef COLON AttributePath
           ( OR ViewableRef COLON AttributePath )* SEMI;

UniquenessConstraint : UNIQUE ( WHERE LogicalExpression COLON )?
            ( GlobalUniqueness | LocalUniqueness ) SEMI;

GlobalUniqueness : UniqueEl ( COMMA UniqueEl )*;

UniqueEl : ObjectOrAttributePath;

LocalUniqueness : LPAR LOCAL RPAR
          Name
          ( MINUS GT Name )* COLON
          Name ( COMMA Name )*;

SetConstraint : SET CONSTRAINT ( WHERE Expression COLON )?
        Expression SEMI;

ConstraintsDef : CONSTRAINTS OF ClassOrAssociationRef EQ
        ( ConstraintDef )*
        END SEMI;

// Expressions

Expression : Term;

Term : Term0 ( EQ GT Term0 )?;
Term0 : Term1 ( ( OR | PLUS | MINUS ) Term1 )*;
Term1 : Term2 ( ( AND | MUL | DIV ) Term2 )*;
Term2 : Predicate ( Relation Predicate )?;

Predicate : ( factor
      | ( NOT )? LPAR Expression RPAR
      | DEFINED LPAR factor RPAR );

Relation : ( EQ EQ | NOT_EQ | LT GT | LTEQ | GTEQ | LT | GT );

factor : ObjectOrAttributePath 
        | (Inspection | INSPECTION InspectionViewableRef) (OF ObjectOrAttributePath)?
        | FunctionCall
        | PARAMETER (ModelName DOT)? RunTimeParameterName
        | Constant;

ObjectOrAttributePath : PathEl (MINUS GT PathEl)*;

AttributePath : ObjectOrAttributePath;

PathEl : THIS
        | THISAREA
        | THATAREA
        | PARENT
        | ReferenceAttributeName
        | AssociationPath
        | RoleName (LSBR AssociationName RSBR)?
        | BaseName
        | AttributeRef;

AssociationPath : ('\\')? AssociationAccessName;

AttributeRef : AttributeName (LSBR (FIRST | LAST | AxisListIndexPosNumber) RSBR)?
              | AGGREGATES;

FunctionCall : (ModelName DOT)? (TopicName DOT)? FunctionName
              LPAR Argument (COMMA Argument)* RPAR;

Argument : Expression
          | ALL (LPAR RestrictedClassOrAssRef | ViewableRef RPAR)?;

// Fonctions

FunctionDef : FUNCTION Name
         LPAR ArgumentDef (COMMA ArgumentDef)* RPAR
         COLON ArgumentType Explanation? SEMI;

ArgumentDef : Name COLON ArgumentType;

ArgumentType : AttrTypeDef
         | (OBJECT | OBJECTS) OF (RestrictedClassOrAssRef | ViewRef)
         | ENUMVAL
         | ENUMTREEVAL;

// Vues

ViewDef : VIEW Name
      PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
      ( FormationDef | EXTENDS ViewRef )?
      BaseExtensionDef*
      Selection*
      EQ
      ViewAttributes?
      ConstraintDef*
      END Name SEMI;

ViewRef : (Name DOT (Name DOT)?)? Name;

FormationDef : Projection 
       | Join 
       | Union 
       | Aggregation
       | Inspection;

Projection : PROJECTION OF RenamedViewableRef;

Join : JOIN OF RenamedViewableRef
     (COMMA RenamedViewableRef (LPAR OR NULL RPAR)?)*;

Union : UNION OF RenamedViewableRef
    (COMMA RenamedViewableRef)*;

Aggregation : AGGREGATION OF RenamedViewableRef
        (ALL | EQUAL LPAR UniqueEl RPAR);

Inspection : (AREA INSPECTION OF RenamedViewableRef
        MINUS GT Name
        (MINUS GT Name)*);

RenamedViewableRef : (Name '~')? ViewableRef;

ViewableRef : (Name DOT (Name DOT)?)?
        (Name
        | Name
        | Name
        | Name);

BaseExtensionDef : BASE Name EXTENDED BY
           RenamedViewableRef (COMMA RenamedViewableRef)*;

Selection : WHERE Expression SEMI;

ViewAttributes : ATTRIBUTE
         ( ALL OF Name SEMI
         | AttributeDef
         | Name
         | PropertyKeyword (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         COLON EQ Expression SEMI );

// Représentations graphiques

GraphicDef : GRAPHIC Name PropertyKeyword? (ABSTRACT | FINAL)?
     (EXTENDS GraphicRef)?
     (BASED ON ViewableRef)? EQ
     (Selection)*
     (DrawingRule)*
     END Name SEMI;

GraphicRef : (Name DOT (Name DOT)?)? Name;

DrawingRule : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
  (OF ClassRef)?
  COLON CondSignParamAssignment (COMMA CondSignParamAssignment)* SEMI;

CondSignParamAssignment : WHERE Expression
        LPAR SignParamAssignment ( SEMI SignParamAssignment )* RPAR;

SignParamAssignment : Name
            COLON EQ ( LCBR MetaObjectRef RCBR
               | factor
               | ACCORDING AttributePath
                LPAR EnumAssignment 
          ( COMMA EnumAssignment )* RPAR );

EnumAssignment : ( LCBR MetaObjectRef RCBR | Constant )
       WHEN IN EnumRange;

EnumRange : EnumerationConst (DOT DOT EnumerationConst)?;
