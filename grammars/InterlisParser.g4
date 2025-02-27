parser grammar InterlisParser;
options { tokenVocab=InterlisLexer; }

// Règle principale

interlis2def : INTERLIS WS Dec SEMI { modeldef };

// Définition du modèle

modeldef : CONTRACTED? (TYPE | REFSYSTEM | SYMBOLOGY)? 
           MODEL Name (LPAR Name RPAR)? 
           AT String 
           VERSION String Explanation? 
           (TRANSLATION OF Name LSBR String RSBR)? EQ 
           (IMPORTS UNQUALIFIED? Name (COMMA UNQUALIFIED? Name)* SEMI)* 
           (MetaDataBasketDef 
           | UnitDef 
           | FunctionDef 
           | LineFormTypeDef 
           | DomainDef 
           | RunTimeParameterDef 
           | ClassDef 
           | StructureDef 
           | TopicDef)* 
           END Name DOT;

// Règles à déplacer dans le Parser

// 1. `INTERLIS2Def`
// 2. `ModelDef`
// 3. `TopicDef`
// 4. `Definitions`
// 5. `TopicRef`
// 6. `ClassDef`
// 7. `StructureDef`
// 8. `ClassRef`
// 9. `ClassOrStructureDef`
// 10. `StructureRef`
// 11. `ClassOrStructureRef`
// 12. `AttributeDef`
// 13. `AttrTypeDef`
// 14. `AttrType`
// 15. `ReferenceAttr`
// 16. `RestrictedClassOrAssRef`
// 17. `ClassOrAssociationRef`
// 18. `RestrictedStructureRef`
// 19. `RestrictedClassOrStructureRef`
// 20. `AssociationDef`
// 21. `AssociationRef`
// 22. `RoleDef`
// 23. `Cardinality`
// 24. `DomainDef`
// 25. `Type`
// 26. `DomainRef`
// 27. `BaseType`
// 28. `Constant`
// 29. `TextType`
// 30. `TextConst`
// 31. `EnumerationType`
// 32. `EnumTreeValueType`
// 33. `Enumeration`
// 34. `EnumElement`
// 35. `EnumerationConst`
// 36. `AlignmentType`
// 37. `BooleanType`
// 38. `NumericType`
// 39. `RefSys`
// 40. `DecConst`
// 41. `NumericConst`
// 42. `FormattedType`
// 43. `FormatDef`
// 44. `BaseAttrRef`
// 45. `FormattedConst`
// 46. `DateTimeType`
// 47. `CoordinateType`
// 48. `RotationDef`
// 49. `NullAxisPosNumber`
// 50. `PiHalfAxisPosNumber`
// 51. `ContextDef`
// 52. `OIDType`
// 53. `BlackboxType`
// 54. `ClassType`
// 55. `AttributeType`
// 56. `ClassConst`
// 57. `AttributePathConst`
// 58. `LineType`
// 59. `LineFormType`
// 60. `ControlPoints`
// 61. `IntersectionDef`
// 62. `LineFormTypeDef`
// 63. `UnitDef`
// 64. `DerivedUnit`
// 65. `ComposedUnit`
// 66. `UnitRef`
// 67. `MetaDataBasketDef`
// 68. `MetaDataBasketRef`
// 69. `MetaObjectRef`
// 70. `ParameterDef`
// 71. `RunTimeParameterDef`
// 72. `ConstraintDef`
// 73. `MandatoryConstraint`
// 74. `PlausibilityConstraint`
// 75. `ExistenceConstraint`
// 76. `UniquenessConstraint`
// 77. `GlobalUniqueness`
// 78. `UniqueEl`
// 79. `LocalUniqueness`
// 80. `SetConstraint`
// 81. `ConstraintsDef`
// 82. `Expression`
// 83. `Term`
// 84. `Term0`
// 85. `Term1`
// 86. `Term2`
// 87. `Predicate`
// 88. `Relation`
// 89. `FunctionDef`
// 90. `ArgumentDef`
// 91. `ArgumentType`
// 92. `ViewDef`
// 93. `ViewRef`
// 94. `FormationDef`
// 95. `Projection`
// 96. `Join`
// 97. `Union`
// 98. `Aggregation`
// 99. `Inspection`
// 100. `RenamedViewableRef`
// 101. `ViewableRef`
// 102. `BaseExtensionDef`
// 103. `Selection`
// 104. `ViewAttributes`
// 105. `GraphicDef`
// 106. `GraphicRef`
// 107. `DrawingRule`
// 108. `CondSignParamAssignment`
// 109. `SignParamAssignment`
// 110. `EnumAssignment`
// 111. `EnumRange`