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
> La ressource ili2c fait intervenir la règle [LineAttrDef](https://github.com/claeis/ili2c/blob/2b206f6f0180d9cb2616804e76bbdc803838698b/ili2c-core/src/main/antlr/ch/interlis/ili2c/parser/syntax23.txt#L268C1-L268C12) qui n'est définie nulle part dans le manuel de référence (eCH-0031).
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

```diff
ViewRef : (ModelName '.' (TopicName '.')?)? ViewName;
```

La définition de la règle `ViewAttributes` intervient 2 dois dans le manuel de référence (eCH-0031) soit aux pages 88 et 91.

Dans la définition de la règle Inspection, la seconde référence à `StructureOrLineAttributeName` ne peut être optionnelle sans quoi la règle peut correspondre à une chaine de charactères vides ce qui n'est pas toléré.

## Names

Modifier les définitions de toutes les règles comportant les tokens suivants car il correspondent tous à la règle Name qu'il n'est pas utile de répéter de multiples fois. Ces non-terminaux ne sont, de plus, jamais définis ce pourquoi des placeholders de type String ont été définis de manière intermédiaire lors du contrôle de la grammaire.

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

- `Factor`
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

Ajouter `DOT: '.';` dans les tokens de base et remplacer partout où cela intervient.
- MINUS: '-';
- PLUS: '+';
- COLON: ':';
- GTEQ: '>=';
- LTEQ: '<=';
- LCBR: '{';
- RCBR: '}';
- LSBR: '[';
- RSBR: ']';


### Mots réservés

Les éléments suivants, doivent être ajoutés aux tokens réservés par souci de cohérence
- ENUM
