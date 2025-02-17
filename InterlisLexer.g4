lexer grammar InterlisLexer;

// Lexer rules
Assign : '=';
Scaling : ('e' | 'E') Number;
LParen : '(';
RParen : ')';
Comma : ',';
Semicolon : ';';
LT : '<';
GT : '>';

//Names
Name : Letter (Letter | Digit | '_')*;
Letter : [A-Za-z];
Digit : [0-9];
HexDigit : [0-9A-Fa-f];

//Character strings
String : '"' ( ~['\\"] | '\\"' | '\\\\' | '\\u' HexDigit HexDigit HexDigit HexDigit )* '"';

//Numbers
PosNumber : Digit+;
Number : ('+' | '-')? PosNumber;
Dec : (Number ('.' PosNumber)? | Float);
Float : ('+' | '-')? '0.' (('1'..'9') PosNumber | '0'*) Scaling;

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
ATTRIBUTE : 'ATTRIBUTE';
ATTRIBUTES : 'ATTRIBUTES';
BAG : 'BAG';
BASE : 'BASED';
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
DOMAIN : 'DOMAIN';
END : 'END';
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
HALIGNEMENT : 'HALIGNEMENT';
HIDING : 'HIDING';
I16 : 'I16';
I32 : 'I32';
IDENT : 'IDENT';
IMPORTS : 'IMPORTS';
IN : 'IN';
INHERITANCE : 'INHERITANCE';
INSPECTION : 'INSPECTION';
INTERLIS : 'INTERLIS';
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
MODEL : 'MODEL';
MTEXT : 'MTEXT';
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
VALIGNEMENT : 'VALIGNEMENT';
VERSION : 'VERSION';
VERTEX : 'VERTEX';
VERTEXINFO : 'VERTEXINFO';
VIEW : 'VIEW';
WHEN : 'WHEN';
WHERE : 'WHERE';
WITH : 'WITH';
WITHOUT : 'WITHOUT';
XMLNS : 'XMLNS';

// Single-line comment
SingleLineComment : '!!' ~[\r\n]*;

//Comment block

BlockComment : '/*' .*? '*/';

// Règle principale
INTERLIS2Def : INTERLIS ' ' Dec Semicolon { ModelDef };

// Définition du modèle

ModelDef : 'CONTRACTED'? ('TYPE' | 'REFSYSTEM' | 'SYMBOLOGY')? 
           'MODEL' Name ('(' Name ')')? 
           'AT' String 
           'VERSION' String Explanation? 
           ('TRANSLATION' 'OF' Name '[' String ']')? '=' 
           ('IMPORTS' 'UNQUALIFIED'? Name (',' 'UNQUALIFIED'? Name)* ';')* 
           (MetaDataBasketDef 
           | UnitDef 
           | FunctionDef 
           | LineFormTypeDef 
           | DomainDef 
           | RunTimeParameterDef 
           | ClassDef 
           | StructureDef 
           | TopicDef)* 
           'END' Name '.';

// Thèmes           

TopicDef : 'VIEW'? 'TOPIC' Name
           PropertyKeyword? (ABSTRACT | FINAL)?
           ('EXTENDS' Name)? '='
           ('BASKET' 'OID' 'AS' Name ';')?
           ('OID' 'AS' Name ';')?
           ('DEPENDS' 'ON' Name (',' Name)* ';')?
           (MetaDataBasketDef 
           | UnitDef 
           | FunctionDef 
           | LineFormTypeDef 
           | DomainDef 
           | RunTimeParameterDef 
           | ClassDef 
           | StructureDef 
           | TopicDef)*
           'END' Name ';';

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

TopicRef : (Name '.')? Name;

// Classes et structures

ClassDef : 'CLASS' Name
             PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
               ('EXTENDS' ClassOrStructureRef)? '='
               (('OID' 'AS' Name | 'NO' 'OID') ';')?
             ClassOrStructureDef
           'END' Name ';';

StructureDef : 'STRUCTURE' Name
                 PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
                   ('EXTENDS' StructureRef)? '='
                 ClassOrStructureDef
               'END' Name ';';


ClassRef : (Name '.' (Name '.')?)? Name;
ClassOrStructureDef : ('ATTRIBUTE' AttributeDef+ | ConstraintDef+ | 'PARAMETER' ParameterDef+)+;

StructureRef : (Name '.' (Name '.')?)? Name;

ClassOrStructureRef : ClassRef | StructureRef;

// Attributs

AttributeDef : 'CONTINUOUS'? 'SUBDIVISION'? 
               Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)? 
               ':' AttrTypeDef 
               (':=' Factor (',' Factor)*)? ';';

AttrTypeDef : 'MANDATORY'? AttrType 
            | ('BAG' | 'LIST') Cardinality? 'OF' RestrictedStructureRef;

AttrType : Type 
         | DomainRef 
         | ReferenceAttr 
         | RestrictedStructureRef;

ReferenceAttr : 'REFERENCE' 'TO' PropertyKeyword? EXTERNAL? RestrictedClassOrAssRef;

RestrictedClassOrAssRef : (ClassOrAssociationRef | 'ANYCLASS') 
                        ('RESTRICTION' '(' ClassOrAssociationRef (',' ClassOrAssociationRef)* ')')?;

ClassOrAssociationRef : ClassRef | AssociationRef;

RestrictedStructureRef : (StructureRef | 'ANYSTRUCTURE') 
                       ('RESTRICTION' '(' StructureRef (',' StructureRef)* ')')?;

RestrictedClassOrStructureRef : (ClassOrStructureRef | 'ANYSTRUCTURE') 
                              ('RESTRICTION' '(' ClassOrStructureRef (',' ClassOrStructureRef)* ')')?;

// Relations vraies / Associations

AssociationDef : 'ASSOCIATION' Name
                     PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | OID)?
                     ('EXTENDS' AssociationRef)?
                     ('DERIVED' 'FROM' Name)? '='
                     (('OID' 'AS' Name | 'NO' 'OID') ';')?
                     RoleDef*
                     ('ATTRIBUTE' AttributeDef*)?
                     ('CARDINALITY' '=' Cardinality ';')?
                     ConstraintDef*
                 'END' Name ';';

AssociationRef : (Name '.' (Name '.')?)? Name;

RoleDef : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | HIDING | ORDERED | EXTERNAL)?
              ('--' | '-<>' | '-<#>') Cardinality?
              RestrictedClassOrAssRef ('OR' RestrictedClassOrAssRef)*
              (':=' Factor)? ';';

Cardinality : '{' ('*' | PosNumber ('..' (PosNumber | '*'))?) '}';

// Domaines de valeurs et constantes

DomainDef : 'DOMAIN' Name PropertyKeyword? (ABSTRACT | FINAL)?
                ('EXTENDS' DomainRef)? '='
                ('MANDATORY'? Type | Type) ';';

Type : BaseType | LineType;

DomainRef : (Name '.' (Name '.')?)? Name;

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

TextType : MTEXT ('*' PosNumber)?
         | TEXT ('*' PosNumber)?
         | NAME
         | URI;

TextConst : String;

// Enumérations

EnumerationType : 'ENUM' '{' EnumElement (',' EnumElement)* '}' ('ORDERED' | 'CIRCULAR')?;

EnumTreeValueType : 'ALL' 'OF' DomainRef;

Enumeration : '(' EnumElement (',' EnumElement)* (':' 'FINAL')? ')';

EnumElement : Name ('.' Name)* (SubEnumeration)?;

EnumerationConst : '#' (Name ('.' Name)* ('.' 'OTHERS')? | 'OTHERS');

// Alignement du texte

AlignmentType : ( 'HALIGNMENT' | 'VALIGNMENT' );

// Boolean

BooleanType : BOOLEAN;

// Types de données numériques

NumericType : (MinDec '..' MaxDec | 'NUMERIC') 'CIRCULAR'?
        ('[' UnitRef ']')?
        ('CLOCKWISE' | 'COUNTERCLOCKWISE' | RefSys)?;

RefSys : '{' RefSysMetaObjectRef ('[' AxisPosNumber ']')? '}'
     | '<' CoordDomainRef ('[' AxisPosNumber ']')? '>';

DecConst : Dec | PI | LNBASE;

NumericConst : DecConst ('[' UnitRef ']')?;

// Domaines de valeurs formatés

FormattedType : 'FORMAT' 'BASED' 'ON' StructureRef FormatDef
        | 'FORMAT' FormattedTypeDomainRef MinString '..' MaxString;

FormatDef : '(' 'INHERITANCE'? NonNumString? (BaseAttrRef NonNumString)* BaseAttrRef NonNumString? ')';

BaseAttrRef : Name ('/' IntPosPosNumber)?
      | Name '/' FormattedDomainRef;

FormattedConst : String;

// Date et heure

DateTimeType : ( DATE | TIMEOFDAY | DATETIME );

// Coordonnées

CoordinateType : 'COORD' NumericType
           (',' NumericType (',' NumericType)?
             (',' RotationDef)?)?;

RotationDef : 'ROTATION' NullAxisPosNumber '->' PiHalfAxisPosNumber;

NullAxisPosNumber : PosNumber;
PiHalfAxisPosNumber : PosNumber;

ContextDef : 'CONTEXT' Name '=' '{' GenericCoordDefDomainRef '=' ConcreteDomainRef ('OR' ConcreteDomainRef)* ';' '}' ';';

// Domaines de valeurs des identifications d’objet

OIDType : OID ( ANY | NumericType | TextType );

// Boîtes noires

BlackboxType : BLACKBOX ( 'XML' | BINARY );

// Domaines de valeurs de classes et chemins d’attributs

ClassType : CLASS
        (RESTRICTION '(' ViewableRef (',' ViewableRef)* ')')?
      | STRUCTURE
        (RESTRICTION '(' ClassOrStructureRef (',' ClassOrStructureRef)* ')')?;

AttributeType : ATTRIBUTE
          (OF (ClassType '.' AttributePath | '@' Name))?
          (RESTRICTION '(' AttrTypeDef (',' AttrTypeDef)* ')')?;

ClassConst : '>' ViewableRef;

AttributePathConst : '>>' (ViewableRef '.')? Name;

// Polylignes

LineType : (DIRECTED POLYLINE | SURFACE | AREA)
       (WITH '(' LineFormType (',' LineFormType)* ')')?
       ControlPoints? IntersectionDef? LineAttrDef?;

LineFormType : STRAIGHTS | ARCS | Name '.' Name;

ControlPoints : VERTEX Name;

IntersectionDef : WITHOUT OVERLAPS '>' Dec;

LineFormTypeDef : LINE FORM '{' LineFormType ':' LineStructure ';' '}';

// Unités composées

UnitDef : UNIT Name
      ('(' ABSTRACT ')')?
      ('[' Name ']')?
      (EXTENDS UnitRef)?
      ('=' (DerivedUnit | ComposedUnit))? ';';

DerivedUnit : (DecConst (('*' | '/') DecConst)*
        | FUNCTION Explanation) '[' UnitRef ']';

ComposedUnit : '(' UnitRef (('*' | '/') UnitRef)* ')';

UnitRef : (Name '.' (Name '.')?)? Name;

// Traitement des méta-objets

MetaDataBasketDef : SIGN | REFSYSTEM BASKET Name
           PropertyKeyword? FINAL?
           ('EXTENDS' MetaDataBasketRef)?
           '~' TopicRef
           (OBJECTS OF Name ':' Name (',' Name)*)? ';';

MetaDataBasketRef : (Name '.' (Name '.')?)? Name;

MetaObjectRef : (MetaDataBasketRef '.')? Name;

// Paramètres

ParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
         ':' (AttrTypeDef | METAOBJECT (OF MetaObjectRef)?) ';';

// Paramètres d’exécution

RunTimeParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
            ':' AttrTypeDef ';';

// Conditions de cohérence

ConstraintDef : MandatoryConstraint
        | PlausibilityConstraint
        | ExistenceConstraint
        | UniquenessConstraint
        | SetConstraint;

MandatoryConstraint : MANDATORY CONSTRAINT LogicalExpression ';';

PlausibilityConstraint : CONSTRAINT
             ( '<=' | '>=' ) PercentageDec '%'
             LogicalExpression ';';

ExistenceConstraint : EXISTENCE CONSTRAINT
           AttributePath REQUIRED IN
           ViewableRef ':' AttributePath
           ( OR ViewableRef ':' AttributePath )* ';';

UniquenessConstraint : UNIQUE ( WHERE LogicalExpression ':' )?
            ( GlobalUniqueness | LocalUniqueness ) ';';

GlobalUniqueness : UniqueEl ( ',' UniqueEl )*;

UniqueEl : ObjectOrAttributePath;

LocalUniqueness : '(' LOCAL ')'
          Name
          ( '->' Name )* ':'
          Name ( ',' Name )*;

SetConstraint : SET CONSTRAINT ( WHERE LogicalExpression ':' )?
        LogicalExpression ';';

ConstraintsDef : CONSTRAINTS OF ClassOrAssociationRef '='
        ( ConstraintDef )*
        END ';';

// Expressions

Expression : Term;

Term : Term0 ( '=>' Term0 )?;
Term0 : Term1 ( ( OR | '+' | '-' ) Term1 )*;
Term1 : Term2 ( ( AND | '*' | '/' ) Term2 )*;
Term2 : Predicate ( Relation Predicate )?;

Predicate : ( Factor
      | ( NOT )? '(' LogicalExpression ')'
      | DEFINED '(' Factor ')' );

Relation : ( '==' | '!=' | '<>' | '<=' | '>=' | '<' | '>' );

// Fonctions

FunctionDef : FUNCTION Name
         '(' ArgumentDef (',' ArgumentDef)* ')'
         ':' ArgumentType Explanation? ';';

ArgumentDef : Name ':' ArgumentType;

ArgumentType : AttrTypeDef
         | (OBJECT | OBJECTS) OF (RestrictedClassOrAssRef | ViewRef)
         | ENUMVAL
         | ENUMTREEVAL;

// Vues

ViewDef : VIEW Name
      PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
      ( FormationDef | 'EXTENDS' ViewRef )?
      BaseExtensionDef*
      Selection*
      '='
      ViewAttributes?
      ConstraintDef*
      END Name ';';

ViewRef : (Name '.' (Name '.')?)? Name;

FormationDef : Projection 
       | Join 
       | Union 
       | Aggregation
       | Inspection;

Projection : 'PROJECTION' 'OF' RenamedViewableRef;

Join : 'JOIN' 'OF' RenamedViewableRef
     (',' RenamedViewableRef ('(' 'OR' 'NULL' ')')?)*;

Union : 'UNION' 'OF' RenamedViewableRef
    (',' RenamedViewableRef)*;

Aggregation : 'AGGREGATION' 'OF' RenamedViewableRef
        ('ALL' | 'EQUAL' '(' UniqueEl ')');

Inspection : ('AREA' 'INSPECTION' 'OF' RenamedViewableRef
        '->' Name
        ('->' Name)*);

RenamedViewableRef : (Name '~')? ViewableRef;

ViewableRef : (Name '.' (Name '.')?)?
        (Name
        | Name
        | Name
        | Name);

BaseExtensionDef : 'BASE' Name 'EXTENDED' 'BY'
           RenamedViewableRef (',' RenamedViewableRef)*;

Selection : 'WHERE' LogicalExpression ';';

ViewAttributes : ATTRIBUTE
         ( ALL OF Name ';'
         | AttributeDef
         | Name
         | PropertyKeyword (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         ':=' Expression ';' );

// Représentations graphiques

GraphicDef : GRAPHIC Name PropertyKeyword? (ABSTRACT | FINAL)?
     (EXTENDS GraphicRef)?
     ('BASED' ON ViewableRef)? '='
     (Selection)*
     (DrawingRule)*
     END Name ';';

GraphicRef : (Name '.' (Name '.')?)? Name;

DrawingRule : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
  (OF SignClassRef)?
  ':' CondSignParamAssignment (',' CondSignParamAssignment)* ';';

CondSignParamAssignment : WHERE LogicalExpression
        '(' SignParamAssignment ( ';' SignParamAssignment )* ')';

SignParamAssignment : Name
            ':=' ( '{' MetaObjectRef '}'
               | Factor
               | ACCORDING EnumAttributePath
                '(' EnumAssignment 
          ( ',' EnumAssignment )* ')' );

EnumAssignment : ( '{' MetaObjectRef '}' | Constant ) 
       WHEN IN EnumRange;

EnumRange : EnumerationConst ('..' EnumerationConst)?;

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
LineStructure: String;
LogicalExpression: String;
PercentageDec: String;
ObjectOrAttributePath: String;
SignClassRef: String;
EnumAttributePath: String;
SignParameterName: String;

// Ignore whitespace
WS : [ \t\r\n]+ -> skip;
