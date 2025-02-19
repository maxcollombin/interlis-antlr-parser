parser grammar InterlisParser;
options { tokenVocab=INTERLISLexer; }

// Parser rules
name : Name;
string : String;
property : Property;
properties : LPAR property (COMMA property)* RPAR;
propertyKeyword : PropertyKeyword LT propertyKeywordElement (COMMA propertyKeywordElement)* GT;
propertyKeywordElement : PropertyKeyword;

explanation : Explanation;
inlelinecomment : SingleLineComment;
blockcomment : BlockComment;

interlis2def : INTERLIS2Def;
