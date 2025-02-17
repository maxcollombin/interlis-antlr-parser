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
         | AttributeConst;
```

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