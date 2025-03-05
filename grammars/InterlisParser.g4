parser grammar InterlisParser;
options { tokenVocab=InterlisLexer; }

// Règle principale

interlis2def : INTERLIS Dec SEMI { modeldef };

// Définition du modèle

modeldef : CONTRACTED? (TYPE | REFSYSTEM | SYMBOLOGY)?
           MODEL Name (LPAR Name RPAR)?
           AT STRING
           VERSION STRING Explanation?
           (TRANSLATION OF Name LSBR STRING RSBR)? EQ
           (IMPORTS UNQUALIFIED? Name (COMMA UNQUALIFIED? Name)* SEMI)*
           (metaDataBasketDef
           | unitDef
           | functionDef
           | lineFormTypeDef
           | domainDef
           | runTimeParameterDef
           | classDef
           | structureDef
           | topicDef)*
           END Name DOT;

// Thèmes

topicDef : VIEW? TOPIC Name
                   PropertyKeyword? (ABSTRACT | FINAL)?
                   (EXTENDS topicRef)? EQ
                   (BASKET OID AS Name SEMI)?
                   (OID AS Name SEMI)?
                   (DEPENDS ON topicRef (COMMA topicRef)* SEMI)?
                   definitions*
                   END Name SEMI;

definitions : metaDataBasketDef
            | unitDef
            | functionDef
            | domainDef
            | classDef
            | structureDef
            | associationDef
            | constraintsDef
            | viewDef
            | graphicDef;

topicRef : (Name DOT)? Name;

// Classes et structures

classDef : CLASS Name
             PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
               (EXTENDS classOrStructureRef)? EQ
               ((OID AS Name | NO OID) SEMI)?
             classOrStructureDef
           END Name SEMI;

structureDef : STRUCTURE Name
                 PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
                   (EXTENDS structureRef)? EQ
                 classOrStructureDef
               END Name SEMI;

classRef : (Name DOT (Name DOT)?)? Name;
classOrStructureDef : (ATTRIBUTE attributeDef+ | constraintDef+ | PARAMETER parameterDef+)+;

structureRef : (Name DOT (Name DOT)?)? Name;

classOrStructureRef : classRef | structureRef;

// Attributs

attributeDef : CONTINUOUS? SUBDIVISION?
               Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
               COLON attrTypeDef
               (COLON EQ factor (COMMA factor)*)? SEMI;

attrTypeDef : MANDATORY? attrType
            | (BAG | LIST) cardinality? OF restrictedStructureRef;

attrType : type
         | domainRef
         | referenceAttr
         | restrictedStructureRef;

referenceAttr : REFERENCE TO PropertyKeyword? EXTERNAL? restrictedClassOrAssRef;

restrictedClassOrAssRef : (classOrAssociationRef | ANYCLASS)
                        (RESTRICTION LPAR classOrAssociationRef (COMMA classOrAssociationRef)* RPAR)?;

classOrAssociationRef : classRef | associationRef;

restrictedStructureRef : (structureRef | ANYSTRUCTURE)
                       (RESTRICTION LPAR structureRef (COMMA structureRef)* RPAR)?;

restrictedClassOrStructureRef : (classOrStructureRef | ANYSTRUCTURE)
                              (RESTRICTION LPAR classOrStructureRef (COMMA classOrStructureRef)* RPAR)?;

// Relations vraies / Associations

associationDef : ASSOCIATION Name
                     PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | OID)?
                     (EXTENDS associationRef)?
                     (DERIVED FROM Name)? EQ
                     ((OID AS Name | NO OID) SEMI)?
                     roleDef*
                     (ATTRIBUTE attributeDef*)?
                     (CARDINALITY EQ cardinality SEMI)?
                     constraintDef*
                 END Name SEMI;

associationRef : (Name DOT (Name DOT)?)? Name;

roleDef : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | HIDING | ORDERED | EXTERNAL)?
              (MINUS MINUS | MINUS LT GT | MINUS LT HASH GT) cardinality?
              restrictedClassOrAssRef (OR restrictedClassOrAssRef)*
              (COLON EQ STRING)? SEMI;

cardinality : LCBR (MUL | PosNumber (DOT DOT (PosNumber | MUL))?) RCBR;

// Domaines de valeurs et constantes

domainDef : DOMAIN Name PropertyKeyword? (ABSTRACT | FINAL)?
                (EXTENDS domainRef)? EQ
                (MANDATORY? type | type) SEMI;

type : baseType | lineType;

domainRef : (Name DOT (Name DOT)?)? Name;

baseType : textType
           | enumerationType
           | enumTreeValueType
           | alignmentType
           | booleanType
           | numericType
           | formattedType
           | coordinateType
           | oIDType
           | blackboxType
           | classType
           | attributeType;

constant : UNDEFINED
         | numericConst
         | textConst
         | formattedConst
         | enumerationConst
         | classConst
         | attributePathConst;

// Chaînes de caractères

textType : MTEXT (MUL PosNumber)?
         | TEXT (MUL PosNumber)?
         | NAME
         | URI;

textConst : STRING;

// Enumérations

enumerationType : ENUM LCBR enumElement (COMMA enumElement)* RCBR (ORDERED | CIRCULAR)?;

enumTreeValueType : ALL OF domainRef;

enumeration : LPAR enumElement (COMMA enumElement)* (COLON FINAL)? RPAR;

enumElement : Name (DOT Name)* (enumeration)?;

enumerationConst : HASH (Name (DOT Name)* (DOT OTHERS)? | OTHERS);

// Alignement du texte

alignmentType : ( HALIGNMENT | VALIGNMENT );

// Boolean

booleanType : BOOLEAN;

// Types de données numériques

numericType : (Dec DOT DOT Dec | NUMERIC) CIRCULAR?
        (LSBR unitRef RSBR)?
        (CLOCKWISE | COUNTERCLOCKWISE | refSys)?;

refSys : LCBR metaObjectRef (LSBR PosNumber RSBR)? RCBR
     | LT domainRef (LSBR PosNumber RSBR)? GT;

decConst : Dec | PI | LNBASE;

numericConst : decConst (LSBR unitRef RSBR)?;

// Domaines de valeurs formatés

formattedType : FORMAT BASED ON structureRef formatDef
        | FORMAT domainRef STRING DOT DOT STRING;

formatDef : LPAR INHERITANCE? STRING? (baseAttrRef STRING)* baseAttrRef STRING? RPAR;

baseAttrRef : Name (DIV PosNumber)?
      | Name DIV domainRef;

formattedConst : STRING;

// Date et heure

dateTimeType : ( DATE | TIMEOFDAY | DATETIME );

// Coordonnées

coordinateType : COORD numericType
           (COMMA numericType (COMMA numericType)?
             (COMMA rotationDef)?)?;

rotationDef : ROTATION PosNumber MINUS GT PosNumber;

contextDef : CONTEXT Name EQ LCBR domainRef EQ domainRef (OR domainRef)* SEMI RCBR SEMI;

// Domaines de valeurs des identifications d’objet

oIDType : OID ( ANY | numericType | textType );

// Boîtes noires

blackboxType : BLACKBOX ( XML | BINARY );

// Domaines de valeurs de classes et chemins d’attributs

classType : CLASS
        (RESTRICTION LPAR viewableRef (COMMA viewableRef)* RPAR)?
      | STRUCTURE
        (RESTRICTION LPAR classOrStructureRef (COMMA classOrStructureRef)* RPAR)?;

attributeType : ATTRIBUTE
          (OF (classType DOT attributePath | AT_SYMBOL Name))?
          (RESTRICTION LPAR attrTypeDef (COMMA attrTypeDef)* RPAR)?;

classConst : GT viewableRef;

attributePathConst : GT GT (viewableRef DOT)? Name;

// Polylignes

lineType : ( DIRECTED? POLYLINE | SURFACE | AREA | DIRECTED? MULTIPOLYLINE | MULTISURFACE | MULTIAREA )
        lineForm? controlPoints? intersectionDef?;

lineForm : WITH LPAR lineFormType { COMMA lineFormType } RPAR;

lineFormType : STRAIGHTS | ARCS | Name DOT Name;

controlPoints : VERTEX Name;

intersectionDef : WITHOUT OVERLAPS GT Dec;

lineFormTypeDef : LINE FORM LCBR Name COLON Name SEMI RCBR;

// Unités composées

unitDef : UNIT Name
      (LPAR ABSTRACT RPAR)?
      (LSBR Name RSBR)?
      (EXTENDS unitRef)?
      (EQ (derivedUnit | composedUnit))? SEMI;

derivedUnit : (decConst ((MUL | DIV) decConst)*
        | FUNCTION Explanation) LSBR unitRef RSBR;

composedUnit : LPAR unitRef ((MUL | DIV) unitRef)* RPAR;

unitRef : (Name DOT (Name DOT)?)? Name;

// Traitement des méta-objets

metaDataBasketDef : SIGN | REFSYSTEM BASKET Name
           PropertyKeyword? FINAL?
           (EXTENDS metaDataBasketRef)?
           TILDE topicRef
           (OBJECTS OF Name COLON Name (COMMA Name)*)? SEMI;

metaDataBasketRef : (Name DOT (Name DOT)?)? Name;

metaObjectRef : (metaDataBasketRef DOT)? Name;

// Paramètres

parameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
         COLON (attrTypeDef | METAOBJECT (OF metaObjectRef)?) SEMI;

// Paramètres d’exécution

runTimeParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
            COLON attrTypeDef SEMI;

// Conditions de cohérence

constraintDef : mandatoryConstraint
        | plausibilityConstraint
        | existenceConstraint
        | uniquenessConstraint
        | setConstraint;

mandatoryConstraint : MANDATORY CONSTRAINT expression SEMI;

plausibilityConstraint : CONSTRAINT
             ( LTEQ | GTEQ ) Dec MOD
             expression SEMI;

existenceConstraint : EXISTENCE CONSTRAINT
           attributePath REQUIRED IN
           viewableRef COLON attributePath
           ( OR viewableRef COLON attributePath )* SEMI;

uniquenessConstraint : UNIQUE ( WHERE expression COLON )?
            ( globalUniqueness | localUniqueness ) SEMI;

globalUniqueness : uniqueEl ( COMMA uniqueEl )*;

uniqueEl : objectOrAttributePath;

localUniqueness : LPAR LOCAL RPAR
          Name
          ( MINUS GT Name )* COLON
          Name ( COMMA Name )*;

setConstraint : SET CONSTRAINT ( WHERE expression COLON )?
        expression SEMI;

constraintsDef : CONSTRAINTS OF classOrAssociationRef EQ
        ( constraintDef )*
        END SEMI;

// Expressions

expression : term;

term : term0 ( EQ GT term0 )?;
term0 : term1 ( ( OR | PLUS | MINUS ) term1 )*;
term1 : term2 ( ( AND | MUL | DIV ) term2 )*;
term2 : predicate ( relation predicate )?;

predicate : ( factor
      | ( NOT )? LPAR expression RPAR
      | DEFINED LPAR factor RPAR );

relation : ( EQ EQ | NOT_EQ | LT GT | LTEQ | GTEQ | LT | GT );

factor : objectOrAttributePath
        | (inspection | INSPECTION viewableRef) (OF objectOrAttributePath)?
        | functionCall
        | PARAMETER (Name DOT)? Name
        | constant;

objectOrAttributePath : pathEl (MINUS GT pathEl)*;

attributePath : objectOrAttributePath;

pathEl : THIS
        | THISAREA
        | THATAREA
        | PARENT
        | Name
        | associationPath
        | Name (LSBR Name RSBR)?
        | Name
        | attributeRef;

associationPath : BACKSLASH? Name;

attributeRef : Name (LSBR (FIRST | LAST | Number) RSBR)?
              | AGGREGATES;

functionCall : (Name DOT)? (Name DOT)? Name
              LPAR argument (COMMA argument)* RPAR;

argument : expression
          | ALL (LPAR restrictedClassOrAssRef | viewableRef RPAR)?;

// Fonctions

functionDef : FUNCTION Name
         LPAR argumentDef (COMMA argumentDef)* RPAR
         COLON argumentType Explanation? SEMI;

argumentDef : Name COLON argumentType;

argumentType : attrTypeDef
         | (OBJECT | OBJECTS) OF (restrictedClassOrAssRef | viewRef)
         | ENUMVAL
         | ENUMTREEVAL;

// Vues

viewDef : VIEW Name
      PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
      ( formationDef | EXTENDS viewRef )?
      baseExtensionDef*
      selection*
      EQ
      viewAttributes?
      constraintDef*
      END Name SEMI;

viewRef : (Name DOT (Name DOT)?)? Name;

formationDef : projection 
       | join 
       | union 
       | aggregation
       | inspection;

projection : PROJECTION OF renamedViewableRef;

join : JOIN OF renamedViewableRef
     (COMMA renamedViewableRef (LPAR OR NULL RPAR)?)*;

union : UNION OF renamedViewableRef
    (COMMA renamedViewableRef)*;

aggregation : AGGREGATION OF renamedViewableRef
        (ALL | EQUAL LPAR uniqueEl RPAR);

inspection : (AREA INSPECTION OF renamedViewableRef
        MINUS GT Name
        (MINUS GT Name)*);

renamedViewableRef : (Name TILDE)? viewableRef;

viewableRef : (Name DOT (Name DOT)?)?
        (Name
        | Name
        | Name
        | Name);

baseExtensionDef : BASE Name EXTENDED BY
           renamedViewableRef (COMMA renamedViewableRef)*;

selection : WHERE expression SEMI;

viewAttributes : ATTRIBUTE
         ( ALL OF Name SEMI
         | attributeDef
         | Name
         | PropertyKeyword (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         COLON EQ expression SEMI );

// Représentations graphiques

graphicDef : GRAPHIC Name PropertyKeyword? (ABSTRACT | FINAL)?
     (EXTENDS graphicRef)?
     (BASED ON viewableRef)? EQ
     (selection)*
     (drawingRule)*
     END Name SEMI;

graphicRef : (Name DOT (Name DOT)?)? Name;

drawingRule : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
  (OF classRef)?
  COLON condSignParamAssignment (COMMA condSignParamAssignment)* SEMI;

condSignParamAssignment : WHERE expression
        LPAR signParamAssignment ( SEMI signParamAssignment )* RPAR;

signParamAssignment : Name
            COLON EQ ( LCBR metaObjectRef RCBR
               | factor
               | ACCORDING attributePath
                LPAR enumAssignment 
          ( COMMA enumAssignment )* RPAR );

enumAssignment : ( LCBR metaObjectRef RCBR | constant )
       WHEN IN enumRange;

enumRange : enumerationConst (DOT DOT enumerationConst)?;
