lexer grammar InterlisLexer;

// Lexer rules
EQ : '=';
NOT_EQ : '!='; // newly added
Scaling : ('e' | 'E') Number;
LPAR : '(';
RPAR : ')';
COMMA : ',';
COLON: ':';
SEMI : ';';
LT : '<';
LTEQ: '<=';
GT : '>';
GTEQ: '>=';
DOT: '.';
MINUS: '-';
PLUS: '+';
LCBR: '{';
RCBR: '}';
LSBR: '[';
RSBR: ']';

//Names
Name : Letter (Letter | Digit | '_')*;
Letter : [A-Za-z];
Digit : [0-9];
HexDigit : [0-9A-Fa-f];

//Character strings
String : '"' ( ~['\\"] | '\\"' | '\\\\' | '\\u' HexDigit HexDigit HexDigit HexDigit )* '"';

//Numbers
PosNumber : Digit+;
Number : (PLUS | MINUS)? PosNumber;
Dec : (Number (DOT PosNumber)? | Float);
Float : (PLUS | MINUS)? '0.' (('1'..'9') PosNumber | '0'*) Scaling;

//Sets of properties
Property : [a-zA-Z0-9_]+;
PropertyKeyword : 'Properties';

// Explanations
Explanation : '//' ~('\n'|'\r')* ('\r'? '\n' | EOF);

// Reserved words and special symbols
ABSTRACT : 'ABSTRACT';
ACCORDING : 'ACCORDING';
AGGREGATES : 'AGGREGATES';
AGGREGATION : 'AGGREGATION';
ALL : 'ALL';
AND : 'AND';
ANY : 'ANY';
ANYCLASS : 'ANYCLASS';
ANYSTRUCTURE : 'ANYSTRUCTURE';
ARCS : 'ARCS';
AREA : 'AREA';
AS : 'AS';
ASSOCIATION : 'ASSOCIATION';
AT : 'AT';
AT_SYMBOL : '@'; // newly added
ATTRIBUTE : 'ATTRIBUTE';
ATTRIBUTES : 'ATTRIBUTES';
BAG : 'BAG';
BASE : 'BASE';
BASED : 'BASED';
BASKET : 'BASKET';
BINARY : 'BINARY';
BLACKBOX : 'BLACKBOX';
BLANK : 'BLANK';
BOOLEAN : 'BOOLEAN';
BY : 'BY';
CARDINALITY : 'CARDINALITY';
CHARSET : 'CHARSET';
CIRCULAR : 'CIRCULAR';
CLASS : 'CLASS';
CLOCKWISE : 'CLOCKWISE';
CODE : 'CODE';
CONSTRAINT : 'CONSTRAINT';
CONSTRAINTS : 'CONSTRAINTS';
CONTEXT : 'CONTEXT';
CONTINUE : 'CONTINUE';
CONTINUOUS : 'CONTINUOUS';
CONTOUR : 'CONTOUR';
CONTRACTED : 'CONTRACTED';
COORD : 'COORD';
COORD2 : 'COORD2';
COORD3 : 'COORD3';
COUNTERCLOCKWISE : 'COUNTERCLOCKWISE';
DATE : 'DATE';
DATETIME : 'DATETIME';
DEFAULT : 'DEFAULT';
DEFERRED : 'DEFERRED';
DEFINED : 'DEFINED';
DEGREES : 'DEGREES';
DEPENDS : 'DEPENDS';
DERIVATIVES : 'DERIVATIVES';
DERIVED : 'DERIVED';
DIM1 : 'DIM1';
DIM2 : 'DIM2';
DIRECTED : 'DIRECTED';
DIV: '/';
DOMAIN : 'DOMAIN';
END : 'END';
ENUM : 'ENUM';
ENUMTREEVAL : 'ENUMTREEVAL';
ENUMVAL : 'ENUMVAL';
EQUAL : 'EQUAL';
EXISTENCE : 'EXISTENCE';
EXTENDED : 'EXTENDED';
EXTENDS : 'EXTENDS';
EXTERNAL : 'EXTERNAL';
FINAL : 'FINAL';
FIRST : 'FIRST';
FIX : 'FIX';
FONT : 'FONT';
FORM : 'FORM';
FORMAT : 'FORMAT';
FREE : 'FREE';
FROM : 'FROM';
FUNCTION : 'FUNCTION';
GENERIC : 'GENERIC';
GENERICS : 'GENERICS';
GRADS : 'GRADS';
GRAPHIC : 'GRAPHIC';
HALIGNMENT : 'HALIGNMENT';
HASH : '#'; // newly added
HIDING : 'HIDING';
I16 : 'I16';
I32 : 'I32';
IDENT : 'IDENT';
IMPORTS : 'IMPORTS';
IN : 'IN';
INHERITANCE : 'INHERITANCE';
INSPECTION : 'INSPECTION';
INTERLIS : 'INTERLIS';
// INTERLIS : 'INTERLIS' [ \t\r\n]+ Dec SEMI;
JOIN : 'JOIN';
LAST : 'LAST';
LINE : 'LINE';
LINEATTR : 'LINEATTR';
LINESIZE : 'LINESIZE';
LIST : 'LIST';
LNBASE : 'LNBASE';
LOCAL : 'LOCAL';
MANDATORY : 'MANDATORY';
METAOBJECT : 'METAOBJECT';
MOD: '%';
MODEL : 'MODEL';
MTEXT : 'MTEXT';
MUL: '*';
MULTIAREA : 'MULTIAREA';
MULTICOORD : 'MULTICOORD';
MULTIPOLYLINE : 'MULTIPOLYLINE';
MULTISURFACE : 'MULTISURFACE';
NAME : 'NAME';
NO : 'NO';
NOINCREMENTALTRANSFER : 'NOINCREMENTALTRANSFER';
NOT : 'NOT';
NULL : 'NULL';
NUMERIC : 'NUMERIC';
OBJECT : 'OBJECT';
OBJECTS : 'OBJECTS';
OF : 'OF';
OID : 'OID';
ON : 'ON';
OPTIONAL : 'OPTIONAL';
OR : 'OR';
ORDERED : 'ORDERED';
OTHERS : 'OTHERS';
OVERLAPS : 'OVERLAPS';
PARAMETER : 'PARAMETER';
PARENT : 'PARENT';
PERIPHERY : 'PERIPHERY';
PI : 'PI';
POLYLINE : 'POLYLINE';
PROJECTION : 'PROJECTION';
RADIANS : 'RADIANS';
REFERENCE : 'REFERENCE';
REFSYS : 'REFSYS';
REFSYSTEM : 'REFSYSTEM';
REQUIRED : 'REQUIRED';
RESTRICTION : 'RESTRICTION';
ROTATION : 'ROTATION';
SET : 'SET';
SIGN : 'SIGN';
STRAIGHTS : 'STRAIGHTS';
STRUCTURE : 'STRUCTURE';
SUBDIVISION : 'SUBDIVISION';
SURFACE : 'SURFACE';
SYMBOLOGY : 'SYMBOLOGY';
TABLE : 'TABLE';
TEXT : 'TEXT';
THATAREA : 'THATAREA';
THIS : 'THIS';
THISAREA : 'THISAREA';
TID : 'TID';
TIDSIZE : 'TIDSIZE';
TILDE : '~'; // newly added
TIMEOFDAY : 'TIMEOFDAY';
TO : 'TO';
TOPIC : 'TOPIC';
TRANSFER : 'TRANSFER';
TRANSIENT : 'TRANSIENT';
TRANSLATION : 'TRANSLATION';
TYPE : 'TYPE';
UNDEFINED : 'UNDEFINED';
UNION : 'UNION';
UNIQUE : 'UNIQUE';
UNIT : 'UNIT';
UNQUALIFIED : 'UNQUALIFIED';
URI : 'URI';
VALIGNMENT : 'VALIGNMENT';
VERSION : 'VERSION';
VERTEX : 'VERTEX';
VERTEXINFO : 'VERTEXINFO';
VIEW : 'VIEW';
WHEN : 'WHEN';
WHERE : 'WHERE';
WITH : 'WITH';
WITHOUT : 'WITHOUT';
XML : 'XML';            
XMLNS : 'XMLNS';

// Single-line comment
SingleLineComment : '!!' ~[\r\n]*;

//Comment block

BlockComment : '/*' .*? '*/';

// Règle principale
// INTERLIS2Def : INTERLIS WS Dec SEMI { ModelDef };

// Définition du modèle

// ModelDef : CONTRACTED? (TYPE | REFSYSTEM | SYMBOLOGY)? 
//            MODEL Name (LPAR Name RPAR)? 
//            AT String 
//            VERSION String Explanation? 
//            (TRANSLATION OF Name LSBR String RSBR)? EQ 
//            (IMPORTS UNQUALIFIED? Name (COMMA UNQUALIFIED? Name)* SEMI)* 
//            (MetaDataBasketDef 
//            | UnitDef 
//            | FunctionDef 
//            | LineFormTypeDef 
//            | DomainDef 
//            | RunTimeParameterDef 
//            | ClassDef 
//            | StructureDef 
//            | TopicDef)* 
//            END Name DOT;

// Thèmes           

TopicDef : VIEW? TOPIC Name
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
           | TopicDef)*
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
               (COLON EQ Factor (COMMA Factor)*)? SEMI;

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
              (COLON EQ Factor)? SEMI;

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

TextConst : String;

// Enumérations

EnumerationType : ENUM LCBR EnumElement (COMMA EnumElement)* RCBR (ORDERED | CIRCULAR)?;

EnumTreeValueType : ALL OF DomainRef;

Enumeration : LPAR EnumElement (COMMA EnumElement)* (COLON FINAL)? RPAR;

EnumElement : Name (DOT Name)* (SubEnumeration)?;

EnumerationConst : HASH (Name (DOT Name)* (DOT OTHERS)? | OTHERS);

// Alignement du texte

AlignmentType : ( HALIGNMENT | VALIGNMENT );

// Boolean

BooleanType : BOOLEAN;

// Types de données numériques

NumericType : (MinDec DOT DOT MaxDec | NUMERIC) CIRCULAR?
        (LSBR UnitRef RSBR)?
        (CLOCKWISE | COUNTERCLOCKWISE | RefSys)?;

RefSys : LCBR RefSysMetaObjectRef (LSBR AxisPosNumber RSBR)? RCBR
     | LT CoordDomainRef (LSBR AxisPosNumber RSBR)? GT;

DecConst : Dec | PI | LNBASE;

NumericConst : DecConst (LSBR UnitRef RSBR)?;

// Domaines de valeurs formatés

FormattedType : FORMAT BASED ON StructureRef FormatDef
        | FORMAT FormattedTypeDomainRef MinString DOT DOT MaxString;

FormatDef : LPAR INHERITANCE? NonNumString? (BaseAttrRef NonNumString)* BaseAttrRef NonNumString? RPAR;

BaseAttrRef : Name (DIV IntPosPosNumber)?
      | Name DIV FormattedDomainRef;

FormattedConst : String;

// Date et heure

DateTimeType : ( DATE | TIMEOFDAY | DATETIME );

// Coordonnées

CoordinateType : COORD NumericType
           (COMMA NumericType (COMMA NumericType)?
             (COMMA RotationDef)?)?;

RotationDef : ROTATION NullAxisPosNumber MINUS GT PiHalfAxisPosNumber;

NullAxisPosNumber : PosNumber;
PiHalfAxisPosNumber : PosNumber;

ContextDef : CONTEXT Name EQ LCBR GenericCoordDefDomainRef EQ ConcreteDomainRef (OR ConcreteDomainRef)* SEMI RCBR SEMI;

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

MandatoryConstraint : MANDATORY CONSTRAINT LogicalExpression SEMI;

PlausibilityConstraint : CONSTRAINT
             ( LTEQ | GTEQ ) PercentageDec MOD
             LogicalExpression SEMI;

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

SetConstraint : SET CONSTRAINT ( WHERE LogicalExpression COLON )?
        LogicalExpression SEMI;

ConstraintsDef : CONSTRAINTS OF ClassOrAssociationRef EQ
        ( ConstraintDef )*
        END SEMI;

// Expressions

Expression : Term;

Term : Term0 ( EQ GT Term0 )?;
Term0 : Term1 ( ( OR | PLUS | MINUS ) Term1 )*;
Term1 : Term2 ( ( AND | MUL | DIV ) Term2 )*;
Term2 : Predicate ( Relation Predicate )?;

Predicate : ( Factor
      | ( NOT )? LPAR LogicalExpression RPAR
      | DEFINED LPAR Factor RPAR );

Relation : ( EQ EQ | NOT_EQ | LT GT | LTEQ | GTEQ | LT | GT );

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

Selection : WHERE LogicalExpression SEMI;

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
  (OF SignClassRef)?
  COLON CondSignParamAssignment (COMMA CondSignParamAssignment)* SEMI;

CondSignParamAssignment : WHERE LogicalExpression
        LPAR SignParamAssignment ( SEMI SignParamAssignment )* RPAR;

SignParamAssignment : Name
            COLON EQ ( LCBR MetaObjectRef RCBR
               | Factor
               | ACCORDING EnumAttributePath
                LPAR EnumAssignment 
          ( COMMA EnumAssignment )* RPAR );

EnumAssignment : ( LCBR MetaObjectRef RCBR | Constant ) 
       WHEN IN EnumRange;

EnumRange : EnumerationConst (DOT DOT EnumerationConst)?;

// Placeholders

Factor: String;
SubEnumeration: String;
MinDec: String;
MaxDec: String;
RefSysMetaObjectRef: String;
AxisPosNumber: String;
CoordDomainRef: String;
FormattedTypeDomainRef: String;
MinString: String;
MaxString: String;
NonNumString: String;
IntPosPosNumber: String;
FormattedDomainRef: String;
GenericCoordDefDomainRef: String;
ConcreteDomainRef: String;
AttributePath: String;
LineAttrDef: String;
LogicalExpression: String;
PercentageDec: String;
ObjectOrAttributePath: String;
SignClassRef: String;
EnumAttributePath: String;
LineForm: String;

// Ignore whitespace
WS : [ \t\r\n]+ -> skip;
