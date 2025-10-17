# Inconsistances de grammaire (E)BNF d'Interlis

Par commodité, la grammaire est réinterprétée sous la forme BNF afin de pouvoir être testée avec [ANTLR](https://www.antlr.org/).

## 3.2.7 Signes particuliers et mots réservés

Analyser si une gestion par Tokens est pertinente. Cela alourdit considérablement la grammaire.

## 3.3 Règle principale

```diff
- INTERLIS2Def = ’INTERLIS’ Version-Dec ’;’
-                { ModelDef }.
+ INTERLIS2Def : INTERLIS ' ' Dec Semicolon { ModelDef };
```

### 3.5.2 Thèmes

Voir s'il est nécessaire de définir la règle suivante (n'intervient pas dans la [ressource](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt) de claeis):

```
GenericRef = GenericCoordType-DomainRef;
```

## 3.8 Domaines de valeurs et constantes

Utiliser le token `UNDEFINED` et non une chaine de characatères au niveau de la règle:

```diff
- Constant : 'UNDEFINED'
+ Constant : UNDEFINED
         | NumericConst
         | TextConst
         | FormattedConst
         | EnumerationConst
         | ClassConst
         | AttributePathConst;
```

> [!NOTE]
> La référence dans la règle `Constant` de la ressource [ili2c](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt) n'est pas bonne. Elle devrait être `AttributePathConst` et non pas `AttributeConst`.


### 3.8.1 Chaînes de caractères

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

`MaxLength-PosNumber` ?

```diff
- TextType = ( 'MTEXT' [ '*' MaxLength-PosNumber ] 
+ TextType : MTEXT ('*' PosNumber)?
-          | 'TEXT' [ '*' MaxLength-PosNumber ]
+          | TEXT ('*' PosNumber)?
-          | 'NAME'
+          | NAME
-          | 'URI' ).
+          | URI;
```

### 3.8.3 Alignement du texte

Est-ce que par cohérence, on ne souhaiterait pas définir `HALIGNMENT` et `VALIGNMENT` dans la section 3.2.7 Signes particuliers et mots réservés.
La règle devrait ensuite être modifiée ainsi:

```diff
- AlignmentType : ( 'HALIGNMENT' | 'VALIGNMENT' );
+ AlignmentType : ( HALIGNMENT | VALIGNMENT );
+ 
```

### 3.8.4 Boolean

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- BooleanType : 'BOOLEAN';
+ BooleanType : BOOLEAN;
```

### 3.8.5 Types de données numériques

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- DecConst : Dec | 'PI' | 'LNBASE';
+ DecConst : Dec | PI | LNBASE;
```

### 3.8.7 Date et heure

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- DateTimeType : ( 'DATE' | 'TIMEOFDAY' | 'DATETIME' );
+ DateTimeType : ( DATE | TIMEOFDAY | DATETIME );
```

> [!NOTE]
> La règle `DateTimeType` manque dans la ressource [ili2c](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt).


### 3.8.8 Coordonnées

> [!NOTE]
> La règle `ContextDef` manque dans la ressource [ili2c](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt)

### 3.8.9 Domaines de valeurs des identifications d’objet

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- OIDType : 'OID' ( 'ANY' | NumericType | TextType );
+ OIDType : OID ( ANY | NumericType | TextType );
```

### 3.8.10 Boîtes noires

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.
Par cohérence, `'XML'` pourrait également être défini comme token.

```diff
- BlackboxType : 'BLACKBOX' ( 'XML' | 'BINARY' );
+ BlackboxType : BLACKBOX ( 'XML' | BINARY );
```

### 3.8.11 Domaines de valeurs de classes et chemins d’attributs

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- ClassType : 'CLASS'
+ ClassType : CLASS
-        ('RESTRICTION' '(' ViewableRef (',' ViewableRef)* ')')?
+        (RESTRICTION '(' ViewableRef (',' ViewableRef)* ')')?
-      | 'STRUCTURE'
+      | STRUCTURE
-        ('RESTRICTION' '(' ClassOrStructureRef (',' ClassOrStructureRef)* ')')?;
+        (RESTRICTION '(' ClassOrStructureRef (',' ClassOrStructureRef)* ')')?;
```

```diff
- AttributeType : 'ATTRIBUTE'
+ AttributeType : ATTRIBUTE
-          ('OF' (ClassType '.' AttributePath | '@' ArgumentName))?
+          (OF (ClassType '.' AttributePath | '@' ArgumentName))?
-          ('RESTRICTION' '(' AttrTypeDef (',' AttrTypeDef)* ')')?;
+          (RESTRICTION '(' AttrTypeDef (',' AttrTypeDef)* ')')?;
```

> [!NOTE]
> La règle `AttributeConst` de la ressource [ili2c](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt) n'est pas bonne. Elle devrait être`AttributePathConst`.

### 3.8.12 Polylignes

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- LineType : ('DIRECTED' 'POLYLINE' | 'SURFACE' | 'AREA')
+ LineType : (DIRECTED POLYLINE | SURFACE | AREA)
-       ('WITH' '(' LineFormType (',' LineFormType)* ')')?
+       (WITH '(' LineFormType (',' LineFormType)* ')')?
       ControlPoints? IntersectionDef? LineAttrDef?;
```

En plus de la réutilisation des token prédéfinis, le dernier token Name ne peut pas être optionnel sans quoi la règle `LineFormType` pourrait correspondre à une chaine vide ce qui n'est pas autorisé.

```diff
- LineFormType : 'STRAIGHTS' | 'ARCS' | (Name '.' Name)?;
+ LineFormType : STRAIGHTS | ARCS | (Name '.' Name);
```

```diff
- ControlPoints : 'VERTEX' Name;
+ ControlPoints : VERTEX Name;
```

```diff
- IntersectionDef : 'WITHOUT' 'OVERLAPS' '>' Dec;
+ IntersectionDef : WITHOUT OVERLAPS '>' Dec;
```

```diff
- LineFormTypeDef : 'LINE' 'FORM' '{' LineFormType ':' LineStructure ';' '}';
+ LineFormTypeDef : LINE FORM '{' LineFormType ':' LineStructure ';' '}';
```

> [!NOTE]
> La ressource ili2c fait intervenir la règle [LineAttrDef](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt#L268C1-L268C12) qui n'est définie nulle part diffdans le manuel de référence (eCH-0031).
> La définition de la règle `LineType` n'y est pas non plus correcte.

### 3.9.3 Unités composées

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- UnitDef : 'UNIT' Name
+ UnitDef : UNIT Name
-      ('(' 'ABSTRACT' ')')?
+      ('(' ABSTRACT ')')?
      ('[' Name ']')?
-      ('EXTENDS' UnitRef)?
+      (EXTENDS UnitRef)?
      ('=' (DerivedUnit | ComposedUnit))? ';';
```

```diff
DerivedUnit : (DecConst (('*' | '/') DecConst)*
-        | 'FUNCTION' Explanation) '[' UnitRef ']';
+        | FUNCTION Explanation) '[' UnitRef ']';
```

## 3.10 Traitement des méta-objets

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- MetaDataBasketDef : 'SIGN' | 'REFSYSTEM' 'BASKET' Name
+ MetaDataBasketDef : SIGN | REFSYSTEM BASKET Name
           PropertyKeyword
           ? FINAL?
           (EXTENDS MetaDataBasketRef)?
           '~' TopicRef
           (OBJECTS OF Name ':' Name (',' Name)*)? ';';
```

### 3.10.2 Paramètres

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- ParameterDef : 'PARAMETER' Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
+ ParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
-         ':' (AttrTypeDef | 'METAOBJECT' ('OF' MetaObjectRef)?) ';';
+         ':' (AttrTypeDef | METAOBJECT (OF MetaObjectRef)?) ';';
```

## 3.11 Paramètres d’exécution

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- RunTimeParameterDef : 'PARAMETER' Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
+ RunTimeParameterDef : PARAMETER Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
            ':' AttrTypeDef ';'; 
```

## 3.12 Conditions de cohérence

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- MandatoryConstraint : 'MANDATORY' 'CONSTRAINT' LogicalExpression ';';
+ MandatoryConstraint : MANDATORY CONSTRAINT LogicalExpression ';';
```

```diff
- PlausibilityConstraint : 'CONSTRAINT'
+ PlausibilityConstraint : CONSTRAINT
             ( '<=' | '>=' ) PercentageDec '%'
             LogicalExpression ';';
```

```diff
- ExistenceConstraint : 'EXISTENCE' 'CONSTRAINT'
+ ExistenceConstraint : EXISTENCE CONSTRAINT
-           AttributePath 'REQUIRED' 'IN'
+           AttributePath REQUIRED IN
           ViewableRef ':' AttributePath
-           ( 'OR' ViewableRef ':' AttributePath )* ';';
+           ( OR ViewableRef ':' AttributePath )* ';';
```

```diff
- UniquenessConstraint : 'UNIQUE' ( 'WHERE' LogicalExpression ':' )?
+ UniquenessConstraint : UNIQUE ( WHERE LogicalExpression ':' )?
            ( GlobalUniqueness | LocalUniqueness ) ';';
```

```diff
- LocalUniqueness : '(' 'LOCAL' ')'
+ LocalUniqueness : '(' LOCAL ')'
          StructureAttributeName
          ( '->' StructureAttributeName )* ':'
          AttributeName ( ',' AttributeName )*;
```

```diff
- SetConstraint : 'SET' 'CONSTRAINT' ( 'WHERE' LogicalExpression ':' )?
+ SetConstraint : SET CONSTRAINT ( WHERE LogicalExpression ':' )?
        LogicalExpression ';';
```

```diff
- ConstraintsDef : 'CONSTRAINTS' 'OF' ClassOrAssociationRef '='
+ ConstraintsDef : CONSTRAINTS OF ClassOrAssociationRef '='
        ( ConstraintDef )*
        'END' ';';
```

### Expressions

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- Term0 : Term1 ( ( 'OR' | '+' | '-' ) Term1 )*;
+ Term0 : Term1 ( ( OR | '+' | '-' ) Term1 )*;
```

```diff
- Term1 : Term2 ( ( 'AND' | '*' | '/' ) Term2 )*;
+ Term1 : Term2 ( ( AND | '*' | '/' ) Term2 )*;
```

```diff
Predicate : ( Factor
-      | ( 'NOT' )? '(' LogicalExpression ')'
+      | ( NOT )? '(' LogicalExpression ')'
-      | 'DEFINED' '(' Factor ')' );
+      | DEFINED '(' Factor ')' );
```

> [!NOTE]
> La règle `Term0` manque dans la ressource ili2c et les règles: [Term](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt#L342), [Term1](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt#L344), [Term2](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt#L346)  n'y sont pas correctement définies.

## 3.14 Fonctions

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
- FunctionDef : 'FUNCTION' Name
+ FunctionDef : FUNCTION Name
         '(' ArgumentDef (',' ArgumentDef)* ')'
         ':' ArgumentType Explanation? ';';
```

```diff
ArgumentType : AttrTypeDef
-         | ('OBJECT' | 'OBJECTS') 'OF' (RestrictedClassOrAssRef | ViewRef)
+         | (OBJECT | OBJECTS) OF (RestrictedClassOrAssRef | ViewRef)
-         | 'ENUMVAL'
+         | ENUMVAL
-         | 'ENUMTREEVAL';
+         | ENUMTREEVAL;
```

### 3.15 Vues

Utiliser les token préalablement définis au lieu d'en définir des nouveaux.

```diff
ViewAttributes : ATTRIBUTE
-         ( 'ALL' 'OF' Base-Name ';'
+         ( ALL OF BaseName ';'
         | AttributeDef
-         | Attribute-Name
+         | AttributeName
         | PropertyKeyword (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         ':=' Expression ';' );
```

Il n'est pas possible de définir des non-terminaux contenant des `-` ce pourquoi il est proposé d'utiliser `BaseName` au lieu de `Base-Name` et `AttributeName` au lieu de `Attribute-Name`. Toutefois, le token `NAME` devrait être utilisé indépendemment de tout élément de syntaxe.

```diff
- ViewAttributes : 'ATTRIBUTE' 
+ ViewAttributes : ATTRIBUTE
-         ( 'ALL' OF Base-Name ';'
+         ( 'ALL' OF BaseName ';'
         | AttributeDef
-         | Attribute-Name
+         | AttributeName
         | PropertyKeyword (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         ':=' Expression ';' );
```

Il n'est pas possible de définir des non-terminaux contenant des `-` ce pourquoi il est proposé d'utiliser `BaseName` au lieu de `Base-Name` et `AttributeName` au lieu de `Attribute-Name`. Toutefois, le token `NAME` devrait être utilisé indépendemment de tout élément de syntaxe.


```diff
- ViewDef : VIEW View-Name
+ ViewDef : VIEW ViewName
      PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
      ( FormationDef | EXTENDS ViewRef )?
      BaseExtensionDef*
      Selection*
      '='
      ViewAttributes?
      ConstraintDef*
-      END View-Name ';';
+      END ViewName ';';
```

Il n'est pas possible de définir des non-terminaux contenant des `-` ce pourquoi il est proposé d'utiliser `ViewName` au lieu de `View-Name` Toutefois, le token `NAME` devrait être utilisé indépendemment de tout élément de syntaxe.

Exemple pour la règle `ViewRef`

```diff
- ViewRef : (Model-Name '.' (Topic-Name '.')?)? View-Name;
+ ViewRef : (ModelName '.' (TopicName '.')?)? ViewName;
```

La définition de la règle `ViewAttributes` intervient 2 dois dans le manuel de référence (eCH-0031) soit aux pages 88 et 91.

Dans la définition de la règle Inspection, la seconde référence à `StructureOrLineAttributeName` ne peut être optionnelle sans quoi la règle peut correspondre à une chaine de charactères vides ce qui n'est pas toléré.

## Names

Modifier les définitions de toutes les règles comportant les tokens suivants car il correspondent tous à la règle `Name` qu'il n'est pas utile de répéter de multiples fois. Ces non-terminaux ne sont, de plus, jamais définis ce pourquoi des placeholders de type String ont été définis de manière intermédiaire lors du contrôle de la grammaire.

- NumericAttribute-Name
- StructureAttribute-Name
- Argument-Name
- Attribute-Name
- Base-Name
- Model-Name
- Topic-Name
- Structure-Name
- Class-Name
- Association-Name
- View-Name
- Graphic-Name
- DrawingRule-Name
- SignParameter-Name
- LineStructure-Name

## Divers

Les règles suivantes ne sont jamais définies dans la grammaire:

- `Sub-Enumeration`
- `Min-Dec`
- `Max-Dec`
- `RefSys-MetaObjectRef`
- `Axis-PosNumber`
- `Coord-DomainRef`
- `FormattedType-DomainRef`
- `Min-String`
- `Max-String`
- `NonNum-String`
- `IntPos-PosNumber`
- `Formatted-DomainRef`
- `GenericCoordDef-DomainRef`
- `ConcreteDomainRef`
- `AttributePath`
- `LineAttrDef`
- `LogicalExpression`
- `PercentageDec`
- `ObjectOrAttributePath`
- `SignClassRef`
- `EnumAttributePath`

Toutes les occurences de `'<'`, `'>'`, `'='`, `'('`, `')'`, `','`, `';'` doivent être rempacées par les tokens liés.

- Ajouter DOT: '.'; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter MINUS: '-'; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter PLUS: '+'; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter COLON: ':'; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter GTEQ: '>='; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter LTEQ: '<='; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter LCBR: '{'; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter RCBR: '}'; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter LSBR: '['; dans les tokens de base et remplacer partout où cela intervient.
- Ajouter RSBR: ']'; dans les tokens de base et remplacer partout où cela intervient.

### Mots réservés

Les éléments suivants, doivent être ajoutés aux tokens réservés par souci de cohérence
- ENUM

### Substitutions

- Remplacer `subEnumeration` (ou `Sub-Enumeration`) qui n'est pas défini par `Enumeration` dans la règle EnumElement:

```diff
- EnumElement : Name (DOT Name)* (subEnumeration)?;
+ EnumElement : Name (DOT Name)* (Enumeration)?;
```

Remplacer `MinDec` et `MaxDec` qui ne sont pas définis par `Dec` dans la règle:

```diff
- NumericType : (MinDec DOT DOT MaxDec | NUMERIC) CIRCULAR?
+ NumericType : (Dec DOT DOT Dec | NUMERIC) CIRCULAR?
        (LSBR UnitRef RSBR)?
        (CLOCKWISE | COUNTERCLOCKWISE | RefSys)?;
```

et effectuer la validation Min, Max avec le parseur.

Remplacer `RefSysMetaObjectRef` (ou `RefSys-MetaObjectRef`) qui n'est pas défini par `MetaObjectRef` dans la règle:

```diff
- RefSys : LCBR RefSysMetaObjectRef (LSBR AxisPosNumber RSBR)? RCBR
+ RefSys : LCBR MetaObjectRef (LSBR AxisPosNumber RSBR)? RCBR
     | LT CoordDomainRef (LSBR AxisPosNumber RSBR)? GT;
```

Remplacer `MinString`& `MaxString` qui ne sont pas définis par STRING dans la règle `FormattedType` et effectuer le contrôle avec le parser 

```diff
FormattedType : FORMAT BASED ON StructureRef FormatDef
-        | FORMAT FormattedTypeDomainRef MinString DOT DOT MaxString;
+        | FORMAT FormattedTypeDomainRef STRING DOT DOT STRING;
```

Remplacer `EnumAttributePath` (ou `Enum-AttributePath`) qui n'est pas défini par `AttributePath` dans la règle:

```diff
SignParamAssignment : Name
            COLON EQ ( LCBR MetaObjectRef RCBR
               | factor
-               | ACCORDING EnumAttributePath
+               | ACCORDING AttributePath
                LPAR EnumAssignment 
          ( COMMA EnumAssignment )* RPAR );
```

Remplacer `AxisPosNumber` (ou `Axis-PosNumber`) qui n'est pas défini par `PosNumber` dans la règle:

```diff
- RefSys : LCBR MetaObjectRef (LSBR AxisPosNumber RSBR)? RCBR
+ RefSys : LCBR MetaObjectRef (LSBR PosNumber RSBR)? RCBR
-     | LT CoordDomainRef (LSBR AxisPosNumber RSBR)? GT;
+     | LT CoordDomainRef (LSBR PosNumber RSBR)? GT;
```
Remplacer `CoordDomainRef` (ou `Coord-DomainRef`) qui n'est pas défini par `DomainRef` dans la règle:

```diff
RefSys : LCBR MetaObjectRef (LSBR PosNumber RSBR)? RCBR
-     | LT CoordDomainRef (LSBR PosNumber RSBR)? GT;
+     | LT DomainRef (LSBR PosNumber RSBR)? GT;
```

Remplacer `FormattedDomainRef` (ou `Formatted-DomainRef`) qui n'est pas défini par `DomainRef` dans la règle suivante:

```diff
BaseAttrRef : Name (DIV IntPosPosNumber)?
-      | Name DIV FormattedDomainRef;
+      | Name DIV DomainRef;
```

Remplacer `ConcreteDomainRef` (ou `Concrete-DomainRef`) qui n'est pas défini par `DomainRef` dans la règle:

```diff
- ContextDef : CONTEXT Name EQ LCBR GenericCoordDefDomainRef EQ ConcreteDomainRef (OR ConcreteDomainRef)* SEMI RCBR SEMI;
+ ContextDef : CONTEXT Name EQ LCBR GenericCoordDefDomainRef EQ DomainRef (OR DomainRef)* SEMI RCBR SEMI;
```
Remplacer `FormattedTypeDomainRef` (`FormattedType-DomainRef`) qui n'est pas défini par `DomainRef` dans le règle:

```diff
FormattedType : FORMAT BASED ON StructureRef FormatDef
-         | FORMAT FormattedTypeDomainRef STRING DOT DOT STRING;
+         | FORMAT DomainRef STRING DOT DOT STRING;
```

Remplacer `IntPosPosNumber` (ou `IntPos-PosNumber`) qui n'est pas défini par `PosNumer` dans la règle

```diff
BaseAttrRef : Name (DIV IntPosPosNumber)?
      | Name DIV DomainRef;
```

Remplacer `NonNumString` (ou `NonNum-String`) qui n'est pas défini par `STRING` dans la règle:

```diff
- FormatDef : LPAR INHERITANCE? NonNumString? (BaseAttrRef NonNumString)* BaseAttrRef NonNumString? RPAR;
+ FormatDef : LPAR INHERITANCE? STRING? (BaseAttrRef STRING)* BaseAttrRef STRING? RPAR;
```

Remplacer `GenericCoordDefDomainRef` (ou `GenericCoordDef-DomainRef`) qui n'est pas défini par `DomainRef` dans la règle:

```diff
- ContextDef : CONTEXT Name EQ LCBR GenericCoordDefDomainRef EQ DomainRef (OR DomainRef)* SEMI RCBR SEMI;
+ ContextDef : CONTEXT Name EQ LCBR DomainRef EQ DomainRef (OR DomainRef)* SEMI RCBR SEMI;
```

Remplacer `PercentageDec` (ou `Percentage-Dec`) qui n'est pas défini par `Dec` dans la règle:

```diff
PlausibilityConstraint : CONSTRAINT
-             ( LTEQ | GTEQ ) PercentageDec MOD
+             ( LTEQ | GTEQ ) Dec MOD
             LogicalExpression SEMI;
``
Remplacer `Sign-ClassRef` (ou `Sign-ClassRef`) qui n'est pas défini par `ClassRef` dans la règle:

```diff
DrawingRule : Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL)?
-  (OF SignClassRef)?
+  (OF ClassRef)?
  COLON CondSignParamAssignment (COMMA CondSignParamAssignment)* SEMI;
```

La règle `LogicalExpression` n'est pas définie dans la grammaire. Nous proposons dans un 1er temps de la remplacer par la règle `Expression`.
Il conviendrait cependant de la définir. Actuellement, cela concerne les règles suivantes:

```diff
- uniquenessConstraint : UNIQUE ( WHERE LogicalExpression COLON )?
+ uniquenessConstraint : UNIQUE ( WHERE expression COLON )?
            ( globalUniqueness | localUniqueness ) SEMI;
```

```diff
- MandatoryConstraint : MANDATORY CONSTRAINT LogicalExpression SEMI;
+ MandatoryConstraint : MANDATORY CONSTRAINT Expression SEMI;
```

```diff
PlausibilityConstraint : CONSTRAINT
             ( LTEQ | GTEQ ) Dec MOD
-             LogicalExpression SEMI;
+             LogicalExpression SEMI;
```

```diff
- SetConstraint : SET CONSTRAINT ( WHERE LogicalExpression COLON )?
+ SetConstraint : SET CONSTRAINT ( WHERE Expression COLON )?
-        LogicalExpression SEMI;
+        Expression SEMI;
```

```diff
Predicate : ( factor
-      | ( NOT )? LPAR LogicalExpression RPAR
+      | ( NOT )? LPAR Expression RPAR
      | DEFINED LPAR factor RPAR );
```

```diff
- Selection : WHERE LogicalExpression SEMI;
+ Selection : WHERE Expression SEMI;
```

```diff
- CondSignParamAssignment : WHERE LogicalExpression
+ CondSignParamAssignment : WHERE LogicalExpression
        LPAR SignParamAssignment ( SEMI SignParamAssignment )* RPAR;
```

### Adapations en relation avec les conventions ANTLR et la distinction entre lexer et parser

Actuellement, la règle `` est considérée comme Lexer par ANTLR du fait qu'elle commande par une majuscule ce qui génère des erreurs lors du parsing. Il convient donc de la renommer en et de remplacer toutes ces occurences à savoir:

```diff
- AttributeDef : CONTINUOUS? SUBDIVISION?
+ attributeDef : CONTINUOUS? SUBDIVISION?
               Name PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
               COLON AttrTypeDef
               (COLON EQ factor (COMMA factor)*)? SEMI;
```

```diff
- ClassOrStructureDef : (ATTRIBUTE AttributeDef+ | ConstraintDef+ | PARAMETER ParameterDef+)+;
+ ClassOrStructureDef : (ATTRIBUTE attributeDef+ | ConstraintDef+ | PARAMETER ParameterDef+)+;
```

```diff
AssociationDef : ASSOCIATION Name
                     PropertyKeyword? (ABSTRACT | EXTENDED | FINAL | OID)?
                     (EXTENDS AssociationRef)?
                     (DERIVED FROM Name)? EQ
                     ((OID AS Name | NO OID) SEMI)?
                     RoleDef*
-                     (ATTRIBUTE AttributeDef*)?
+                     (ATTRIBUTE attributeDef*)?
                     (CARDINALITY EQ Cardinality SEMI)?
                     ConstraintDef*
                 END Name SEMI;
```

```diff
ViewAttributes : ATTRIBUTE
         ( ALL OF Name SEMI
-         | AttributeDef
+         | attributeDef
         | Name
         | PropertyKeyword (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         COLON EQ Expression SEMI );
```

Il en est de même pour toutes les autres règles du Parser.

#### Simplification de la grammaire

Dans la règle ``, il n'est pas nécessaire de faire référence à `nullAxisPosNumber`et `piHalfAxisPosNumber` qui se rapportent tous deux au même token `PosNumber` qui peuvent être gérés par le parser.

```diff
- rotationDef : ROTATION nullAxisPosNumber MINUS GT piHalfAxisPosNumber;
+ rotationDef : ROTATION PosNumber MINUS GT PosNumber;
```

```diff
- nullAxisPosNumber : PosNumber;
- piHalfAxisPosNumber : PosNumber;
```

La règle factor doit être adaptée comme suit:

```diff
factor : objectOrAttributePath 
-        | (inspection | INSPECTION InspectionViewableRef) (OF objectOrAttributePath)?
+        | (inspection | INSPECTION viewableRef) (OF objectOrAttributePath)?
        | functionCall
-        | PARAMETER (ModelName DOT)? RunTimeParameterName
+        | PARAMETER (Name DOT)? Name
        | constant;
```

Les règles suivantes pourraient encore être supprimées mais il convient de vérifier avec le parser:

- textConst
- booleanType
- formattedConst
- expression

#### Ordre des règles

Faire attention à l'ordre dans lequel interviennent les règles dans le lexer (les nombres p.ex. doivent intervenir avant les noms car PosNumber utilise Digit)

La règle `numericType` n'est pas cohérente et doit être changée.

```diff
+numeric : (PosNumber HexDigit PosNumber | Dec HexDigit Dec);
+
-numericType : (Dec DOT DOT Dec | NUMERIC) CIRCULAR?
+numericType : NUMERIC? numeric CIRCULAR?
        (LSBR unitRef RSBR)?
        (CLOCKWISE | COUNTERCLOCKWISE | refSys)?;
```

### 3.2.5 Ensembles de propriétés - Eigenschaftsmengen

Les `Property-Keyword`ne devraient idéalement pas être définis dans la grammaire mais dans le parser uniquement.

### XXX

Rajouter SEMI dans la déifinition de la VIEW

```diff
viewDef : VIEW Name
--      Properties? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
++      Properties? (ABSTRACT | EXTENDED | FINAL | TRANSIENT)? SEMI
      ( formationDef | EXTENDS viewRef )?
      baseExtensionDef*
      selection*
      EQ
      viewAttributes?
      constraintDef*
      END Name SEMI;
```

##### formationDef

```diff
-- projection : PROJECTION OF renamedViewableRef;
++ projection : PROJECTION_OF renamedViewableRef SEMI;
```

```diff
--join : JOIN OF renamedViewableRef
++join : JOIN_OF renamedViewableRef
--     (COMMA renamedViewableRef (LPAR OR NULL RPAR)?)*;
++     (COMMA renamedViewableRef (LPAR OR NULL RPAR)?)* SEMI;
```

```diff
-- union : UNION OF renamedViewableRef
++ union : UNION_OF renamedViewableRef
--    (COMMA renamedViewableRef)*;
++    (COMMA renamedViewableRef)* SEMI;
```

```diff
-- aggregation : AGGREGATION OF renamedViewableRef
++ aggregation : AGGREGATION_OF renamedViewableRef
--        (ALL | EQUAL LPAR uniqueEl RPAR);
++        (ALL | EQUAL LPAR uniqueEl RPAR) SEMI;
```

```diff
-- inspection : (AREA INSPECTION OF renamedViewableRef
++ inspection : (AREA INSPECTION_OF renamedViewableRef
        MINUS GT Name
--        (MINUS GT Name)*);
++        (MINUS GT Name)*) SEMI;
```

> [!NOTE]
> Cela implique également de définir les tokens: `PROJECTION_OF` , `JOIN_OF` , `UNION_OF` , `AGGREGATION_OF` , `INSPECTION_OF`
> Tous les tokens associés sans le `OF` devraient, en principe, pouvoir être supprimés.
> On pourrait aussi définir les tokens sous la forme projection : 'PROJECTION_OF';

##### viewAttributes

La règle viewAttribute doit être modifiée pour permeetre l'utilisation du token `ASSIGN` (:=) qu'elle ne permet pas en l'état. Elle doit aussi être modifiée pour permettre d'utiliser plusieurs attributs. Ce qui, une nouvelle fois n'est pas le cas en l'état

```diff
viewAttributes : ATTRIBUTE?
         ( ALL OF Name SEMI
         | attributeDef
--       | Name
++       | (Name ASSIGN expression SEMI)+
         | Properties (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
         COLON EQ expression SEMI );
```

La règle actuelle pour des nombres flottants est trop restrictive est implique qu'ils doivent nécessairement commencer par `0`.

Ainsi, il serait judicieux de la modifier comme suit:

```diff
-- Float : (PLUS | MINUS)? '0.' (('1'..'9') PosNumber | '0'*) Scaling;
++ Float : (PLUS | MINUS)? Digit+ (DOT Digit+)? Scaling?;
```

> [!WARNING]
> Il y a des problèmes importants dans la définition des nombres (conflits entre `Dec` et `PosNumber`)
> Faire une comparaison avec la grammaire CartoSym


## 3.6 Attributs - Attribute

Les règles `attributeDef` et `` doivent être modifier pour inclure les parenthpses entre le properies keywords

```diff
attributeDef : CONTINUOUS? SUBDIVISION?
--               Name (ABSTRACT | EXTENDED | FINAL | TRANSIENT)?
++               Name (LPAR(ABSTRACT | EXTENDED | FINAL | TRANSIENT)RPAR)?
               COLON attrTypeDef
               (ASSIGN? factor (COMMA factor)*)? SEMI;
```

```diff
-- referenceAttr : REFERENCE TO (EXTERNAL )? restrictedClassOrAssRef;
++ referenceAttr : REFERENCE TO (LPAR EXTERNAL RPAR)? restrictedClassOrAssRef;
```

Dans certains modèles (comme p.e.x [Axis_V1_1.ili](https://models.geo.admin.ch/ASTRA/Axis_V1_1.ili)) , INTERLIS est utilisé pour définir des attributs ce qui rentre en conflit avec le token et les règles `interlis2def` et `attributeDef`. 

> [!NOTE]
> ili2c permet de valider un modèle avec DEPENDS ON model1.topic1 ; DEPENDS ON model1.topic2 ce qui n'est pas correct par rapport à la grammaire. L'input correct est DEPENDS ON model1.topic1, model1.topic2;

## // 3.8 Domaines de valeurs et constantes - Wertebereiche und Konstanten


```diff
domainDef : DOMAIN Name (ABSTRACT | FINAL)?
                (EXTENDS domainRef)? EQ
--                (MANDATORY? type | type ) SEMI;
++                (MANDATORY? type | type | enumeration) SEMI;
```

Ajouter la règle enumeration à la règle domainDef afin de pouvoir permettre les énumerations dans les DOMAIN.

// 3.8.5 Types de données numériques - Numerische Datentypen

Modifier la règle numeric pour permettre toutes les comibnaisons possibles avec ou sans les signes:

```diff
-- numeric : (PosNumber DOTDOT PosNumber | Dec DOTDOT Dec);
++ numeric : (Number DOTDOT Number | Number DOTDOT PosNumber | PosNumber DOTDOT PosNumber| Dec DOTDOT Dec);
```

## 3.16 Représentations graphiques

Modification de la règle pour gérer le cas où la clause WHERE est absente:

```diff
- condSignParamAssignment : WHERE? expression 
+ condSignParamAssignment : (WHERE? expression)? 
        LPAR signParamAssignment ( SEMI signParamAssignment )* RPAR;
```

## 3.6 Attributs - Attribute

Ajout de la règle type à la règle restrictedStructureRef


```diff
- restrictedStructureRef : (structureRef | ANYSTRUCTURE)
+ restrictedStructureRef : (structureRef | type | ANYSTRUCTURE)
                       (RESTRICTION LPAR structureRef (COMMA structureRef)* RPAR)?;
```

afin de permettre des inputs tels que:

```bash
INTERLIS 2.4;

MODEL ModelA AT "http://www.interlis.ch/ili2c/tests/" VERSION "1" =
	TOPIC TopicA =
		CLASS ClassA =
			attrA : LIST {0..*} OF TEXT*20; !! ok in 2.4
		END ClassA;
	END TopicA;
END ModelA.
```

## 3.9.3 Unités composées - Zusammengesetzte Einheiten

Ajout du caractère optionnel à UNIT dans la règle unitDef de manière à ne pas avoir à systématiquement répéter UNIT pour chaque unité.

```diff
- unitDef : UNIT Name
+ unitDef : UNIT? Name
      (LPAR ABSTRACT RPAR)?
      (LSBR Name RSBR)?
      (EXTENDS unitRef)?
      (EQ (derivedUnit | composedUnit))? SEMI;
```

ajout de INTERLIS à la règle unitRef 

```diff
unitRef : (Name DOT (Name DOT)?)? Name
+        | (INTERLIS DOT  Name);
```

pour permettre INTERLIS. dans les unités


## 3.8 Domaines de valeurs et constantes - Wertebereiche und Konstanten

```diff
domainDef : DOMAIN? Name (LPAR (ABSTRACT | FINAL | GENERIC) RPAR)?
                (EXTENDS domainRef)? EQ
-                ((MANDATORY? type | type | enumeration) COMMA)* SEMI;
+                ((MANDATORY? type | type | enumeration) COMMA?)* SEMI;
```

Ajout d'un option pour la virgule dans la définition des DOMAIN de manière à permettre des inputs tels que :

```bash
  DOMAIN
    BasketOID = OID TEXT;  !! Filename
```

## 3.5.2 Thèmes - Themen

Modification de la règle `topicDef`:

```diff
topicDef : VIEW? TOPIC Name
                   (LPAR (ABSTRACT | FINAL) RPAR)?
                   (EXTENDS topicRef)? EQ
-                   (BASKET OID AS Name SEMI)?
+                   (BASKET? OID AS (Name | Name DOT Name) SEMI)?
-                   (OID AS Name SEMI)?
+                   (OID AS (Name | Name DOT Name) SEMI)?
                   (DEPENDS ON topicRef (COMMA topicRef)* SEMI)?
                   definitions*
                   END Name SEMI;
```

afin de pouvoir gérer des inputs tels que :

```bash
TOPIC ModelData =
 BASKET OID AS IlisMeta16.BasketOID;
  OID AS IlisMeta16.MetaElemOID;
  [...]
END ModelData;
```

extraits de [IlisMeta16.ili](https://github.com/claeis/ili2c/blob/master/standard/IlisMeta16.ili)

## 3.8.6 Domaines de valeurs formatés - Formatierte Wertebereiche

```diff
-formattedType : FORMAT BASED_ON structureRef formatDef
+formattedType : FORMAT INTERLIS DOT Name STRING DOTDOT STRING
+              | FORMAT BASED_ON structureRef formatDef
              | FORMAT domainRef STRING DOTDOT STRING;
```

Modification de la règle des domaines de valeurs formattées pour pouvoir intégrer le token INTERLIS

## 3.8 Domaines de valeurs et constantes

Ajouter la règle dateTimeType à la règle baseType

```diff
baseType : textType
           | enumerationType
           | enumTreeValueType
           | alignmentType
           | booleanType
           | numericType
           | formattedType
+          | dateTimeType
           | coordinateType
           | oIDType
           | blackboxType
           | classType
           | attributeType;
```

## (Lexer) Tokens non définis dans le Parser

Les tokens suivants ne semblement pas être définis dans le parser: 

BLANK
CODE
CONTINUE
CONTOUR
DEFAULT
DERIVATIVES
FIX
FONT
FREE
GRADS
IDENT
OPTIONAL
PERIPHERY
RADIANS
TABLE
TID
TIDSIZE
VERTEXINFO
