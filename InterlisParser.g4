parser grammar InterlisParser;
options { tokenVocab=INTERLISLexer; }

// Parser rules
name : Name;
string : String;
property : Property;
properties : LParen property (Comma property)* RParen;
propertyKeyword : PropertyKeyword LT propertyKeywordElement (Comma propertyKeywordElement)* GT;
propertyKeywordElement : PropertyKeyword;

explanation : Explanation;
inlelinecomment : SingleLineComment;
blockcomment : BlockComment;

interlis2def : INTERLIS2Def;