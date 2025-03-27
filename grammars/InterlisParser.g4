parser grammar InterlisParser;
options { tokenVocab=InterlisLexer; }

// Règles syntaxiques INTERLIS 2.4 définies avec les référénce eCH-0031
// INTERLIS 2.4 Syntaxregeln definiert mit eCH-0031-Referenzen

// 3.3 Règle principale - Hauptregel

interlis2def : INTERLIS Dec SEMI modeldef?;

// 3.5 Modèles, thèmes, classes - Modelle, Themen, Klassen
// 3.5.1 Modèles - Modelle

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

// 3.5.2 Thèmes - Themen

topicDef : VIEW? TOPIC Name
                   Properties? (ABSTRACT | FINAL)?
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

// 3.5.3 Classes et structures - Klassen und Strukturen

classDef : CLASS Name
             Properties? (ABSTRACT | EXTENDED | FINAL)?
               (EXTENDS classOrStructureRef)? EQ
               ((OID AS Name | NO OID) SEMI)?
             classOrStructureDef
           END Name SEMI;

structureDef : STRUCTURE Name
                 Properties? (ABSTRACT | EXTENDED | FINAL)?
                   (EXTENDS structureRef)? EQ
                 classOrStructureDef
               END Name SEMI;

classRef : (Name DOT (Name DOT)?)? Name;
classOrStructureDef : (ATTRIBUTE? attributeDef+ | constraintDef+ | PARAMETER? parameterDef+)+;

structureRef : (Name DOT (Name DOT)?)? Name;

classOrStructureRef : classRef | structureRef;

// 3.6 Attributs - Attribute

attributeDef : CONTINUOUS? SUBDIVISION?
               Name Properties? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
               COLON attrTypeDef
               (ASSIGN? factor (COMMA factor)*)? SEMI;

attrTypeDef : MANDATORY? attrType
            | (BAG | LIST) cardinality? OF restrictedStructureRef;

attrType : type
         | domainRef
         | referenceAttr
         | restrictedStructureRef;

referenceAttr : REFERENCE TO Properties? EXTERNAL? restrictedClassOrAssRef;

restrictedClassOrAssRef : (classOrAssociationRef | ANYCLASS)
                        (RESTRICTION LPAR classOrAssociationRef (COMMA classOrAssociationRef)* RPAR)?;

classOrAssociationRef : classRef | associationRef;

restrictedStructureRef : (structureRef | ANYSTRUCTURE)
                       (RESTRICTION LPAR structureRef (COMMA structureRef)* RPAR)?;

restrictedClassOrStructureRef : (classOrStructureRef | ANYSTRUCTURE)
                              (RESTRICTION LPAR classOrStructureRef (COMMA classOrStructureRef)* RPAR)?;

// 3.7 Relations vraies - Eigentliche Beziehungen
//3.7.1 Description des relations - Beschreibung von Beziehungen

associationDef : ASSOCIATION Name
                     Properties? (ABSTRACT | EXTENDED | FINAL | OID)?
                     (EXTENDS associationRef)?
                     (DERIVED FROM Name)? EQ
                     ((OID AS Name | NO OID) SEMI)?
                     roleDef*
                     (ATTRIBUTE attributeDef*)?
                     (CARDINALITY EQ cardinality SEMI)?
                     constraintDef*
                 END Name SEMI;

associationRef : (Name DOT (Name DOT)?)? Name;

roleDef : Name Properties? (ABSTRACT | EXTENDED | FINAL | HIDING | ORDERED | EXTERNAL)?
              (MINUS MINUS | MINUS LT GT | MINUS LT HASH GT) cardinality?
              restrictedClassOrAssRef (OR restrictedClassOrAssRef)*
              (COLON EQ STRING)? SEMI;

cardinality : LCBR (MUL | PosNumber (DOTDOT (PosNumber | MUL))?) RCBR;

// 3.8 Domaines de valeurs et constantes - Wertebereiche und Konstanten

domainDef : DOMAIN Name Properties? (ABSTRACT | FINAL)?
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

// 3.8.1 Chaînes de caractères - Zeichenketten

textType : MTEXT (MUL PosNumber)?
         | TEXT (MUL PosNumber)?
         | NAME
         | URI;

textConst : STRING;

// 3.8.2 Enumérations - Aufzählungen

enumerationType : ENUM LCBR enumElement (COMMA enumElement)* RCBR (ORDERED | CIRCULAR)?;

enumTreeValueType : ALL OF domainRef;

enumeration : LPAR enumElement (COMMA enumElement)* (COLON FINAL)? RPAR;

enumElement : Name (DOT Name)* (enumeration)?;

enumerationConst : HASH (Name (DOT Name)* (DOT OTHERS)? | OTHERS);

// 3.8.3 Alignement du texte - Textausrichtungen

alignmentType : ( HALIGNMENT | VALIGNMENT );

// 3.8.4 Boolean - Boolean

booleanType : BOOLEAN;

// 3.8.5 Types de données numériques - Numerische Datentypen

numeric : (PosNumber DOTDOT PosNumber | Dec DOTDOT Dec);

numericType : NUMERIC? numeric CIRCULAR?
        (LSBR unitRef RSBR)?
        (CLOCKWISE | COUNTERCLOCKWISE | refSys)?;

refSys : LCBR metaObjectRef (LSBR PosNumber RSBR)? RCBR
     | LT domainRef (LSBR PosNumber RSBR)? GT;

decConst : Dec | PI | LNBASE;

numericConst : decConst (LSBR unitRef RSBR)?;

// 3.8.6 Domaines de valeurs formatés - Formatierte Wertebereiche

formattedType : FORMAT BASED ON structureRef formatDef
        | FORMAT domainRef STRING DOT DOT STRING;

formatDef : LPAR INHERITANCE? STRING? (baseAttrRef STRING)* baseAttrRef STRING? RPAR;

baseAttrRef : Name (DIV PosNumber)?
      | Name DIV domainRef;

formattedConst : STRING;

// 3.8.7 Date et heure - Datum und Zeit

dateTimeType : ( DATE | TIMEOFDAY | DATETIME );

// 3.8.8 Coordonnées - Koordinaten

coordinateType : COORD numericType
           (COMMA numericType (COMMA numericType)?
             (COMMA rotationDef)?)?;

rotationDef : ROTATION PosNumber MINUS GT PosNumber;

contextDef : CONTEXT Name EQ LCBR domainRef EQ domainRef (OR domainRef)* SEMI RCBR SEMI;

// 3.8.9 Domaines de valeurs des identifications d’objet - Wertebereiche von Objektidentifikationen

oIDType : OID ( ANY | numericType | textType );

// 3.8.10 Boîtes noires - Gefässe

blackboxType : BLACKBOX ( XML | BINARY );

// 3.8.11 Domaines de valeurs de classes et chemins d’attributs - Wertebereiche von Klassen und Attributpfaden

classType : CLASS
        (RESTRICTION LPAR viewableRef (COMMA viewableRef)* RPAR)?
      | STRUCTURE
        (RESTRICTION LPAR classOrStructureRef (COMMA classOrStructureRef)* RPAR)?;

attributeType : ATTRIBUTE
          (OF (classType DOT attributePath | AT_SYMBOL Name))?
          (RESTRICTION LPAR attrTypeDef (COMMA attrTypeDef)* RPAR)?;

classConst : GT viewableRef;

attributePathConst : GT GT (viewableRef DOT)? Name;

// 3.8.12 Polylignes - Linienzüge
// 3.8.12.2 Polyligne comportant des segments de droite et des arcs de cercle en tant qu’éléments de portion de courbe prédéfinis
// 3.8.12.2 Linienzug mit Strecken und Kreisbogen als vordefinierte Kurvenstücke

lineType : ( DIRECTED? POLYLINE | SURFACE | AREA | DIRECTED? MULTIPOLYLINE | MULTISURFACE | MULTIAREA )
        lineForm? controlPoints? intersectionDef?;

lineForm : WITH LPAR lineFormType { COMMA lineFormType } RPAR;

lineFormType : STRAIGHTS | ARCS | Name DOT Name;

controlPoints : VERTEX Name;

intersectionDef : WITHOUT OVERLAPS GT Dec;

// 3.8.12.3 Formes de portions de courbes supplémentaires - Weitere Kurvenstück-Formen

lineFormTypeDef : LINE FORM LCBR Name COLON Name SEMI RCBR;

// 3.9 Unités - Einheiten

// 3.9.3 Unités composées - Zusammengesetzte Einheiten

unitDef : UNIT Name
      (LPAR ABSTRACT RPAR)?
      (LSBR Name RSBR)?
      (EXTENDS unitRef)?
      (EQ (derivedUnit | composedUnit))? SEMI;

derivedUnit : (decConst ((MUL | DIV) decConst)*
        | FUNCTION Explanation) LSBR unitRef RSBR;

composedUnit : LPAR unitRef ((MUL | DIV) unitRef)* RPAR;

unitRef : (Name DOT (Name DOT)?)? Name;

// 3.10 Traitement des méta-objets - Umgang mit Metaobjekten

metaDataBasketDef : SIGN | REFSYSTEM BASKET Name
           Properties? FINAL?
           (EXTENDS metaDataBasketRef)?
           TILDE topicRef
           (OBJECTS OF Name COLON Name (COMMA Name)*)? SEMI;

metaDataBasketRef : (Name DOT (Name DOT)?)? Name;

metaObjectRef : (metaDataBasketRef DOT)? Name;

// 3.10.2 Paramètres - Parameter
// 3.10.2.2 Paramètres des signatures - Parameter von Signaturen

parameterDef : PARAMETER Name Properties? (ABSTRACT | EXTENDED | FINAL)?
         COLON (attrTypeDef | METAOBJECT (OF metaObjectRef)?) SEMI;

// 3.11 Paramètres d’exécution - Laufzeitparameter

runTimeParameterDef : PARAMETER Name Properties? (ABSTRACT | EXTENDED | FINAL)?
            COLON attrTypeDef SEMI;

// 3.12 Conditions de cohérence - Konsistenzbedingungen

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

// 3.13 Expressions - Ausdrücke

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

// 3.14 Fonctions

functionDef : FUNCTION Name
         LPAR argumentDef (COMMA argumentDef)* RPAR
         COLON argumentType Explanation? SEMI;

argumentDef : Name COLON argumentType;

argumentType : attrTypeDef
         | (OBJECT | OBJECTS) OF (restrictedClassOrAssRef | viewRef)
         | ENUMVAL
         | ENUMTREEVAL;

// 3.15 Vues

viewDef : VIEW Name
        Properties? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
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

projection : PROJECTION_OF renamedViewableRef SEMI;

join : JOIN_OF renamedViewableRef
     (COMMA renamedViewableRef (LPAR OR NULL RPAR)?)* SEMI;

union : UNION_OF renamedViewableRef
    (COMMA renamedViewableRef)* SEMI;

aggregation : AGGREGATION_OF renamedViewableRef
        (ALL | EQUAL LPAR uniqueEl RPAR) SEMI;

inspection : (AREA INSPECTION_OF renamedViewableRef
        MINUS GT Name
        (MINUS GT Name)*) SEMI;

renamedViewableRef : (Name TILDE)? viewableRef;

viewableRef : (Name DOT (Name DOT)?)?
        (Name
        | Name
        | Name
        | Name);

baseExtensionDef : BASE Name EXTENDED BY
           renamedViewableRef (COMMA renamedViewableRef)*;

selection : WHERE expression SEMI;

viewAttributes : ATTRIBUTE?
         ( ALL OF Name SEMI
         | attributeDef
         | Name
         | Properties (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         COLON EQ expression SEMI );

// 3.16 Représentations graphiques

graphicDef : GRAPHIC Name Properties? (ABSTRACT | FINAL)?
     (EXTENDS graphicRef)?
     (BASED ON viewableRef)? EQ
     (selection)*
     (drawingRule)*
     END Name SEMI;

graphicRef : (Name DOT (Name DOT)?)? Name;

drawingRule : Name Properties? (ABSTRACT | EXTENDED | FINAL)?
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
