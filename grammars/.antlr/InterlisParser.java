// Generated from /home/maxime/Desktop/interlis-antlr-parser/grammars/InterlisParser.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class InterlisParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		EQ=1, NOT_EQ=2, Scaling=3, LPAR=4, RPAR=5, COMMA=6, COLON=7, SEMI=8, LT=9, 
		LTEQ=10, GT=11, GTEQ=12, DOT=13, MINUS=14, PLUS=15, LCBR=16, RCBR=17, 
		LSBR=18, RSBR=19, Name=20, Letter=21, Digit=22, HexDigit=23, String=24, 
		PosNumber=25, Number=26, Dec=27, Float=28, Property=29, PropertyKeyword=30, 
		Explanation=31, ABSTRACT=32, ACCORDING=33, AGGREGATES=34, AGGREGATION=35, 
		ALL=36, AND=37, ANY=38, ANYCLASS=39, ANYSTRUCTURE=40, ARCS=41, AREA=42, 
		AS=43, ASSOCIATION=44, AT=45, AT_SYMBOL=46, ATTRIBUTE=47, ATTRIBUTES=48, 
		BAG=49, BASE=50, BASED=51, BASKET=52, BINARY=53, BLACKBOX=54, BLANK=55, 
		BOOLEAN=56, BY=57, CARDINALITY=58, CHARSET=59, CIRCULAR=60, CLASS=61, 
		CLOCKWISE=62, CODE=63, CONSTRAINT=64, CONSTRAINTS=65, CONTEXT=66, CONTINUE=67, 
		CONTINUOUS=68, CONTOUR=69, CONTRACTED=70, COORD=71, COORD2=72, COORD3=73, 
		COUNTERCLOCKWISE=74, DATE=75, DATETIME=76, DEFAULT=77, DEFERRED=78, DEFINED=79, 
		DEGREES=80, DEPENDS=81, DERIVATIVES=82, DERIVED=83, DIM1=84, DIM2=85, 
		DIRECTED=86, DIV=87, DOMAIN=88, END=89, ENUM=90, ENUMTREEVAL=91, ENUMVAL=92, 
		EQUAL=93, EXISTENCE=94, EXTENDED=95, EXTENDS=96, EXTERNAL=97, FINAL=98, 
		FIRST=99, FIX=100, FONT=101, FORM=102, FORMAT=103, FREE=104, FROM=105, 
		FUNCTION=106, GENERIC=107, GENERICS=108, GRADS=109, GRAPHIC=110, HALIGNMENT=111, 
		HASH=112, HIDING=113, I16=114, I32=115, IDENT=116, IMPORTS=117, IN=118, 
		INHERITANCE=119, INSPECTION=120, INTERLIS=121, JOIN=122, LAST=123, LINE=124, 
		LINEATTR=125, LINESIZE=126, LIST=127, LNBASE=128, LOCAL=129, MANDATORY=130, 
		METAOBJECT=131, MOD=132, MODEL=133, MTEXT=134, MUL=135, MULTIAREA=136, 
		MULTICOORD=137, MULTIPOLYLINE=138, MULTISURFACE=139, NAME=140, NO=141, 
		NOINCREMENTALTRANSFER=142, NOT=143, NULL=144, NUMERIC=145, OBJECT=146, 
		OBJECTS=147, OF=148, OID=149, ON=150, OPTIONAL=151, OR=152, ORDERED=153, 
		OTHERS=154, OVERLAPS=155, PARAMETER=156, PARENT=157, PERIPHERY=158, PI=159, 
		POLYLINE=160, PROJECTION=161, RADIANS=162, REFERENCE=163, REFSYS=164, 
		REFSYSTEM=165, REQUIRED=166, RESTRICTION=167, ROTATION=168, SET=169, SIGN=170, 
		STRAIGHTS=171, STRUCTURE=172, SUBDIVISION=173, SURFACE=174, SYMBOLOGY=175, 
		TABLE=176, TEXT=177, THATAREA=178, THIS=179, THISAREA=180, TID=181, TIDSIZE=182, 
		TILDE=183, TIMEOFDAY=184, TO=185, TOPIC=186, TRANSFER=187, TRANSIENT=188, 
		TRANSLATION=189, TYPE=190, UNDEFINED=191, UNION=192, UNIQUE=193, UNIT=194, 
		UNQUALIFIED=195, URI=196, VALIGNMENT=197, VERSION=198, VERTEX=199, VERTEXINFO=200, 
		VIEW=201, WHEN=202, WHERE=203, WITH=204, WITHOUT=205, XML=206, XMLNS=207, 
		SingleLineComment=208, BlockComment=209, TopicDef=210, Definitions=211, 
		TopicRef=212, ClassDef=213, StructureDef=214, ClassRef=215, ClassOrStructureDef=216, 
		StructureRef=217, ClassOrStructureRef=218, AttributeDef=219, AttrTypeDef=220, 
		AttrType=221, ReferenceAttr=222, RestrictedClassOrAssRef=223, ClassOrAssociationRef=224, 
		RestrictedStructureRef=225, RestrictedClassOrStructureRef=226, AssociationDef=227, 
		AssociationRef=228, RoleDef=229, Cardinality=230, DomainDef=231, Type=232, 
		DomainRef=233, BaseType=234, Constant=235, TextType=236, TextConst=237, 
		EnumerationType=238, EnumTreeValueType=239, Enumeration=240, EnumElement=241, 
		EnumerationConst=242, AlignmentType=243, BooleanType=244, NumericType=245, 
		RefSys=246, DecConst=247, NumericConst=248, FormattedType=249, FormatDef=250, 
		BaseAttrRef=251, FormattedConst=252, DateTimeType=253, CoordinateType=254, 
		RotationDef=255, NullAxisPosNumber=256, PiHalfAxisPosNumber=257, ContextDef=258, 
		OIDType=259, BlackboxType=260, ClassType=261, AttributeType=262, ClassConst=263, 
		AttributePathConst=264, LineType=265, LineFormType=266, ControlPoints=267, 
		IntersectionDef=268, LineFormTypeDef=269, UnitDef=270, DerivedUnit=271, 
		ComposedUnit=272, UnitRef=273, MetaDataBasketDef=274, MetaDataBasketRef=275, 
		MetaObjectRef=276, ParameterDef=277, RunTimeParameterDef=278, ConstraintDef=279, 
		MandatoryConstraint=280, PlausibilityConstraint=281, ExistenceConstraint=282, 
		UniquenessConstraint=283, GlobalUniqueness=284, UniqueEl=285, LocalUniqueness=286, 
		SetConstraint=287, ConstraintsDef=288, Expression=289, Term=290, Term0=291, 
		Term1=292, Term2=293, Predicate=294, Relation=295, FunctionDef=296, ArgumentDef=297, 
		ArgumentType=298, ViewDef=299, ViewRef=300, FormationDef=301, Projection=302, 
		Join=303, Union=304, Aggregation=305, Inspection=306, RenamedViewableRef=307, 
		ViewableRef=308, BaseExtensionDef=309, Selection=310, ViewAttributes=311, 
		GraphicDef=312, GraphicRef=313, DrawingRule=314, CondSignParamAssignment=315, 
		SignParamAssignment=316, EnumAssignment=317, EnumRange=318, Factor=319, 
		SubEnumeration=320, MinDec=321, MaxDec=322, RefSysMetaObjectRef=323, AxisPosNumber=324, 
		CoordDomainRef=325, FormattedTypeDomainRef=326, MinString=327, MaxString=328, 
		NonNumString=329, IntPosPosNumber=330, FormattedDomainRef=331, GenericCoordDefDomainRef=332, 
		ConcreteDomainRef=333, AttributePath=334, LineAttrDef=335, LogicalExpression=336, 
		PercentageDec=337, ObjectOrAttributePath=338, SignClassRef=339, EnumAttributePath=340, 
		LineForm=341, WS=342;
	public static final int
		RULE_interlis2def = 0, RULE_modeldef = 1;
	private static String[] makeRuleNames() {
		return new String[] {
			"interlis2def", "modeldef"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'='", "'!='", null, "'('", "')'", "','", "':'", "';'", "'<'", 
			"'<='", "'>'", "'>='", "'.'", "'-'", "'+'", "'{'", "'}'", "'['", "']'", 
			null, null, null, null, null, null, null, null, null, null, "'Properties'", 
			null, "'ABSTRACT'", "'ACCORDING'", "'AGGREGATES'", "'AGGREGATION'", "'ALL'", 
			"'AND'", "'ANY'", "'ANYCLASS'", "'ANYSTRUCTURE'", "'ARCS'", "'AREA'", 
			"'AS'", "'ASSOCIATION'", "'AT'", "'@'", "'ATTRIBUTE'", "'ATTRIBUTES'", 
			"'BAG'", "'BASE'", "'BASED'", "'BASKET'", "'BINARY'", "'BLACKBOX'", "'BLANK'", 
			"'BOOLEAN'", "'BY'", "'CARDINALITY'", "'CHARSET'", "'CIRCULAR'", "'CLASS'", 
			"'CLOCKWISE'", "'CODE'", "'CONSTRAINT'", "'CONSTRAINTS'", "'CONTEXT'", 
			"'CONTINUE'", "'CONTINUOUS'", "'CONTOUR'", "'CONTRACTED'", "'COORD'", 
			"'COORD2'", "'COORD3'", "'COUNTERCLOCKWISE'", "'DATE'", "'DATETIME'", 
			"'DEFAULT'", "'DEFERRED'", "'DEFINED'", "'DEGREES'", "'DEPENDS'", "'DERIVATIVES'", 
			"'DERIVED'", "'DIM1'", "'DIM2'", "'DIRECTED'", "'/'", "'DOMAIN'", "'END'", 
			"'ENUM'", "'ENUMTREEVAL'", "'ENUMVAL'", "'EQUAL'", "'EXISTENCE'", "'EXTENDED'", 
			"'EXTENDS'", "'EXTERNAL'", "'FINAL'", "'FIRST'", "'FIX'", "'FONT'", "'FORM'", 
			"'FORMAT'", "'FREE'", "'FROM'", "'FUNCTION'", "'GENERIC'", "'GENERICS'", 
			"'GRADS'", "'GRAPHIC'", "'HALIGNMENT'", "'#'", "'HIDING'", "'I16'", "'I32'", 
			"'IDENT'", "'IMPORTS'", "'IN'", "'INHERITANCE'", "'INSPECTION'", "'INTERLIS'", 
			"'JOIN'", "'LAST'", "'LINE'", "'LINEATTR'", "'LINESIZE'", "'LIST'", "'LNBASE'", 
			"'LOCAL'", "'MANDATORY'", "'METAOBJECT'", "'%'", "'MODEL'", "'MTEXT'", 
			"'*'", "'MULTIAREA'", "'MULTICOORD'", "'MULTIPOLYLINE'", "'MULTISURFACE'", 
			"'NAME'", "'NO'", "'NOINCREMENTALTRANSFER'", "'NOT'", "'NULL'", "'NUMERIC'", 
			"'OBJECT'", "'OBJECTS'", "'OF'", "'OID'", "'ON'", "'OPTIONAL'", "'OR'", 
			"'ORDERED'", "'OTHERS'", "'OVERLAPS'", "'PARAMETER'", "'PARENT'", "'PERIPHERY'", 
			"'PI'", "'POLYLINE'", "'PROJECTION'", "'RADIANS'", "'REFERENCE'", "'REFSYS'", 
			"'REFSYSTEM'", "'REQUIRED'", "'RESTRICTION'", "'ROTATION'", "'SET'", 
			"'SIGN'", "'STRAIGHTS'", "'STRUCTURE'", "'SUBDIVISION'", "'SURFACE'", 
			"'SYMBOLOGY'", "'TABLE'", "'TEXT'", "'THATAREA'", "'THIS'", "'THISAREA'", 
			"'TID'", "'TIDSIZE'", "'~'", "'TIMEOFDAY'", "'TO'", "'TOPIC'", "'TRANSFER'", 
			"'TRANSIENT'", "'TRANSLATION'", "'TYPE'", "'UNDEFINED'", "'UNION'", "'UNIQUE'", 
			"'UNIT'", "'UNQUALIFIED'", "'URI'", "'VALIGNMENT'", "'VERSION'", "'VERTEX'", 
			"'VERTEXINFO'", "'VIEW'", "'WHEN'", "'WHERE'", "'WITH'", "'WITHOUT'", 
			"'XML'", "'XMLNS'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "EQ", "NOT_EQ", "Scaling", "LPAR", "RPAR", "COMMA", "COLON", "SEMI", 
			"LT", "LTEQ", "GT", "GTEQ", "DOT", "MINUS", "PLUS", "LCBR", "RCBR", "LSBR", 
			"RSBR", "Name", "Letter", "Digit", "HexDigit", "String", "PosNumber", 
			"Number", "Dec", "Float", "Property", "PropertyKeyword", "Explanation", 
			"ABSTRACT", "ACCORDING", "AGGREGATES", "AGGREGATION", "ALL", "AND", "ANY", 
			"ANYCLASS", "ANYSTRUCTURE", "ARCS", "AREA", "AS", "ASSOCIATION", "AT", 
			"AT_SYMBOL", "ATTRIBUTE", "ATTRIBUTES", "BAG", "BASE", "BASED", "BASKET", 
			"BINARY", "BLACKBOX", "BLANK", "BOOLEAN", "BY", "CARDINALITY", "CHARSET", 
			"CIRCULAR", "CLASS", "CLOCKWISE", "CODE", "CONSTRAINT", "CONSTRAINTS", 
			"CONTEXT", "CONTINUE", "CONTINUOUS", "CONTOUR", "CONTRACTED", "COORD", 
			"COORD2", "COORD3", "COUNTERCLOCKWISE", "DATE", "DATETIME", "DEFAULT", 
			"DEFERRED", "DEFINED", "DEGREES", "DEPENDS", "DERIVATIVES", "DERIVED", 
			"DIM1", "DIM2", "DIRECTED", "DIV", "DOMAIN", "END", "ENUM", "ENUMTREEVAL", 
			"ENUMVAL", "EQUAL", "EXISTENCE", "EXTENDED", "EXTENDS", "EXTERNAL", "FINAL", 
			"FIRST", "FIX", "FONT", "FORM", "FORMAT", "FREE", "FROM", "FUNCTION", 
			"GENERIC", "GENERICS", "GRADS", "GRAPHIC", "HALIGNMENT", "HASH", "HIDING", 
			"I16", "I32", "IDENT", "IMPORTS", "IN", "INHERITANCE", "INSPECTION", 
			"INTERLIS", "JOIN", "LAST", "LINE", "LINEATTR", "LINESIZE", "LIST", "LNBASE", 
			"LOCAL", "MANDATORY", "METAOBJECT", "MOD", "MODEL", "MTEXT", "MUL", "MULTIAREA", 
			"MULTICOORD", "MULTIPOLYLINE", "MULTISURFACE", "NAME", "NO", "NOINCREMENTALTRANSFER", 
			"NOT", "NULL", "NUMERIC", "OBJECT", "OBJECTS", "OF", "OID", "ON", "OPTIONAL", 
			"OR", "ORDERED", "OTHERS", "OVERLAPS", "PARAMETER", "PARENT", "PERIPHERY", 
			"PI", "POLYLINE", "PROJECTION", "RADIANS", "REFERENCE", "REFSYS", "REFSYSTEM", 
			"REQUIRED", "RESTRICTION", "ROTATION", "SET", "SIGN", "STRAIGHTS", "STRUCTURE", 
			"SUBDIVISION", "SURFACE", "SYMBOLOGY", "TABLE", "TEXT", "THATAREA", "THIS", 
			"THISAREA", "TID", "TIDSIZE", "TILDE", "TIMEOFDAY", "TO", "TOPIC", "TRANSFER", 
			"TRANSIENT", "TRANSLATION", "TYPE", "UNDEFINED", "UNION", "UNIQUE", "UNIT", 
			"UNQUALIFIED", "URI", "VALIGNMENT", "VERSION", "VERTEX", "VERTEXINFO", 
			"VIEW", "WHEN", "WHERE", "WITH", "WITHOUT", "XML", "XMLNS", "SingleLineComment", 
			"BlockComment", "TopicDef", "Definitions", "TopicRef", "ClassDef", "StructureDef", 
			"ClassRef", "ClassOrStructureDef", "StructureRef", "ClassOrStructureRef", 
			"AttributeDef", "AttrTypeDef", "AttrType", "ReferenceAttr", "RestrictedClassOrAssRef", 
			"ClassOrAssociationRef", "RestrictedStructureRef", "RestrictedClassOrStructureRef", 
			"AssociationDef", "AssociationRef", "RoleDef", "Cardinality", "DomainDef", 
			"Type", "DomainRef", "BaseType", "Constant", "TextType", "TextConst", 
			"EnumerationType", "EnumTreeValueType", "Enumeration", "EnumElement", 
			"EnumerationConst", "AlignmentType", "BooleanType", "NumericType", "RefSys", 
			"DecConst", "NumericConst", "FormattedType", "FormatDef", "BaseAttrRef", 
			"FormattedConst", "DateTimeType", "CoordinateType", "RotationDef", "NullAxisPosNumber", 
			"PiHalfAxisPosNumber", "ContextDef", "OIDType", "BlackboxType", "ClassType", 
			"AttributeType", "ClassConst", "AttributePathConst", "LineType", "LineFormType", 
			"ControlPoints", "IntersectionDef", "LineFormTypeDef", "UnitDef", "DerivedUnit", 
			"ComposedUnit", "UnitRef", "MetaDataBasketDef", "MetaDataBasketRef", 
			"MetaObjectRef", "ParameterDef", "RunTimeParameterDef", "ConstraintDef", 
			"MandatoryConstraint", "PlausibilityConstraint", "ExistenceConstraint", 
			"UniquenessConstraint", "GlobalUniqueness", "UniqueEl", "LocalUniqueness", 
			"SetConstraint", "ConstraintsDef", "Expression", "Term", "Term0", "Term1", 
			"Term2", "Predicate", "Relation", "FunctionDef", "ArgumentDef", "ArgumentType", 
			"ViewDef", "ViewRef", "FormationDef", "Projection", "Join", "Union", 
			"Aggregation", "Inspection", "RenamedViewableRef", "ViewableRef", "BaseExtensionDef", 
			"Selection", "ViewAttributes", "GraphicDef", "GraphicRef", "DrawingRule", 
			"CondSignParamAssignment", "SignParamAssignment", "EnumAssignment", "EnumRange", 
			"Factor", "SubEnumeration", "MinDec", "MaxDec", "RefSysMetaObjectRef", 
			"AxisPosNumber", "CoordDomainRef", "FormattedTypeDomainRef", "MinString", 
			"MaxString", "NonNumString", "IntPosPosNumber", "FormattedDomainRef", 
			"GenericCoordDefDomainRef", "ConcreteDomainRef", "AttributePath", "LineAttrDef", 
			"LogicalExpression", "PercentageDec", "ObjectOrAttributePath", "SignClassRef", 
			"EnumAttributePath", "LineForm", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "InterlisParser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public InterlisParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class Interlis2defContext extends ParserRuleContext {
		public TerminalNode INTERLIS() { return getToken(InterlisParser.INTERLIS, 0); }
		public TerminalNode WS() { return getToken(InterlisParser.WS, 0); }
		public TerminalNode Dec() { return getToken(InterlisParser.Dec, 0); }
		public TerminalNode SEMI() { return getToken(InterlisParser.SEMI, 0); }
		public Interlis2defContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_interlis2def; }
	}

	public final Interlis2defContext interlis2def() throws RecognitionException {
		Interlis2defContext _localctx = new Interlis2defContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_interlis2def);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4);
			match(INTERLIS);
			setState(5);
			match(WS);
			setState(6);
			match(Dec);
			setState(7);
			match(SEMI);
			 modeldef 
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ModeldefContext extends ParserRuleContext {
		public TerminalNode MODEL() { return getToken(InterlisParser.MODEL, 0); }
		public List<TerminalNode> Name() { return getTokens(InterlisParser.Name); }
		public TerminalNode Name(int i) {
			return getToken(InterlisParser.Name, i);
		}
		public TerminalNode AT() { return getToken(InterlisParser.AT, 0); }
		public List<TerminalNode> String() { return getTokens(InterlisParser.String); }
		public TerminalNode String(int i) {
			return getToken(InterlisParser.String, i);
		}
		public TerminalNode VERSION() { return getToken(InterlisParser.VERSION, 0); }
		public TerminalNode EQ() { return getToken(InterlisParser.EQ, 0); }
		public TerminalNode END() { return getToken(InterlisParser.END, 0); }
		public TerminalNode DOT() { return getToken(InterlisParser.DOT, 0); }
		public TerminalNode CONTRACTED() { return getToken(InterlisParser.CONTRACTED, 0); }
		public TerminalNode LPAR() { return getToken(InterlisParser.LPAR, 0); }
		public TerminalNode RPAR() { return getToken(InterlisParser.RPAR, 0); }
		public TerminalNode Explanation() { return getToken(InterlisParser.Explanation, 0); }
		public TerminalNode TRANSLATION() { return getToken(InterlisParser.TRANSLATION, 0); }
		public TerminalNode OF() { return getToken(InterlisParser.OF, 0); }
		public TerminalNode LSBR() { return getToken(InterlisParser.LSBR, 0); }
		public TerminalNode RSBR() { return getToken(InterlisParser.RSBR, 0); }
		public List<TerminalNode> IMPORTS() { return getTokens(InterlisParser.IMPORTS); }
		public TerminalNode IMPORTS(int i) {
			return getToken(InterlisParser.IMPORTS, i);
		}
		public List<TerminalNode> SEMI() { return getTokens(InterlisParser.SEMI); }
		public TerminalNode SEMI(int i) {
			return getToken(InterlisParser.SEMI, i);
		}
		public TerminalNode TYPE() { return getToken(InterlisParser.TYPE, 0); }
		public TerminalNode REFSYSTEM() { return getToken(InterlisParser.REFSYSTEM, 0); }
		public TerminalNode SYMBOLOGY() { return getToken(InterlisParser.SYMBOLOGY, 0); }
		public List<TerminalNode> MetaDataBasketDef() { return getTokens(InterlisParser.MetaDataBasketDef); }
		public TerminalNode MetaDataBasketDef(int i) {
			return getToken(InterlisParser.MetaDataBasketDef, i);
		}
		public List<TerminalNode> UnitDef() { return getTokens(InterlisParser.UnitDef); }
		public TerminalNode UnitDef(int i) {
			return getToken(InterlisParser.UnitDef, i);
		}
		public List<TerminalNode> FunctionDef() { return getTokens(InterlisParser.FunctionDef); }
		public TerminalNode FunctionDef(int i) {
			return getToken(InterlisParser.FunctionDef, i);
		}
		public List<TerminalNode> LineFormTypeDef() { return getTokens(InterlisParser.LineFormTypeDef); }
		public TerminalNode LineFormTypeDef(int i) {
			return getToken(InterlisParser.LineFormTypeDef, i);
		}
		public List<TerminalNode> DomainDef() { return getTokens(InterlisParser.DomainDef); }
		public TerminalNode DomainDef(int i) {
			return getToken(InterlisParser.DomainDef, i);
		}
		public List<TerminalNode> RunTimeParameterDef() { return getTokens(InterlisParser.RunTimeParameterDef); }
		public TerminalNode RunTimeParameterDef(int i) {
			return getToken(InterlisParser.RunTimeParameterDef, i);
		}
		public List<TerminalNode> ClassDef() { return getTokens(InterlisParser.ClassDef); }
		public TerminalNode ClassDef(int i) {
			return getToken(InterlisParser.ClassDef, i);
		}
		public List<TerminalNode> StructureDef() { return getTokens(InterlisParser.StructureDef); }
		public TerminalNode StructureDef(int i) {
			return getToken(InterlisParser.StructureDef, i);
		}
		public List<TerminalNode> TopicDef() { return getTokens(InterlisParser.TopicDef); }
		public TerminalNode TopicDef(int i) {
			return getToken(InterlisParser.TopicDef, i);
		}
		public List<TerminalNode> UNQUALIFIED() { return getTokens(InterlisParser.UNQUALIFIED); }
		public TerminalNode UNQUALIFIED(int i) {
			return getToken(InterlisParser.UNQUALIFIED, i);
		}
		public List<TerminalNode> COMMA() { return getTokens(InterlisParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(InterlisParser.COMMA, i);
		}
		public ModeldefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_modeldef; }
	}

	public final ModeldefContext modeldef() throws RecognitionException {
		ModeldefContext _localctx = new ModeldefContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_modeldef);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(11);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CONTRACTED) {
				{
				setState(10);
				match(CONTRACTED);
				}
			}

			setState(14);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (((((_la - 165)) & ~0x3f) == 0 && ((1L << (_la - 165)) & 33555457L) != 0)) {
				{
				setState(13);
				_la = _input.LA(1);
				if ( !(((((_la - 165)) & ~0x3f) == 0 && ((1L << (_la - 165)) & 33555457L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
			}

			setState(16);
			match(MODEL);
			setState(17);
			match(Name);
			setState(21);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==LPAR) {
				{
				setState(18);
				match(LPAR);
				setState(19);
				match(Name);
				setState(20);
				match(RPAR);
				}
			}

			setState(23);
			match(AT);
			setState(24);
			match(String);
			setState(25);
			match(VERSION);
			setState(26);
			match(String);
			setState(28);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==Explanation) {
				{
				setState(27);
				match(Explanation);
				}
			}

			setState(36);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==TRANSLATION) {
				{
				setState(30);
				match(TRANSLATION);
				setState(31);
				match(OF);
				setState(32);
				match(Name);
				setState(33);
				match(LSBR);
				setState(34);
				match(String);
				setState(35);
				match(RSBR);
				}
			}

			setState(38);
			match(EQ);
			setState(57);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==IMPORTS) {
				{
				{
				setState(39);
				match(IMPORTS);
				setState(41);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==UNQUALIFIED) {
					{
					setState(40);
					match(UNQUALIFIED);
					}
				}

				setState(43);
				match(Name);
				setState(51);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==COMMA) {
					{
					{
					setState(44);
					match(COMMA);
					setState(46);
					_errHandler.sync(this);
					_la = _input.LA(1);
					if (_la==UNQUALIFIED) {
						{
						setState(45);
						match(UNQUALIFIED);
						}
					}

					setState(48);
					match(Name);
					}
					}
					setState(53);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(54);
				match(SEMI);
				}
				}
				setState(59);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(63);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (((((_la - 210)) & ~0x3f) == 0 && ((1L << (_la - 210)) & 1729382256912367641L) != 0) || ((((_la - 274)) & ~0x3f) == 0 && ((1L << (_la - 274)) & 4194321L) != 0)) {
				{
				{
				setState(60);
				_la = _input.LA(1);
				if ( !(((((_la - 210)) & ~0x3f) == 0 && ((1L << (_la - 210)) & 1729382256912367641L) != 0) || ((((_la - 274)) & ~0x3f) == 0 && ((1L << (_la - 274)) & 4194321L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				}
				}
				setState(65);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(66);
			match(END);
			setState(67);
			match(Name);
			setState(68);
			match(DOT);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u0156G\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0001\u0003\u0001\f\b\u0001\u0001\u0001\u0003\u0001\u000f\b\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003\u0001\u0016"+
		"\b\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003"+
		"\u0001\u001d\b\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0003\u0001%\b\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0003\u0001*\b\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0003"+
		"\u0001/\b\u0001\u0001\u0001\u0005\u00012\b\u0001\n\u0001\f\u00015\t\u0001"+
		"\u0001\u0001\u0005\u00018\b\u0001\n\u0001\f\u0001;\t\u0001\u0001\u0001"+
		"\u0005\u0001>\b\u0001\n\u0001\f\u0001A\t\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0001\u0000\u0000\u0002\u0000\u0002\u0000"+
		"\u0002\u0003\u0000\u00a5\u00a5\u00af\u00af\u00be\u00be\u0007\u0000\u00d2"+
		"\u00d2\u00d5\u00d6\u00e7\u00e7\u010d\u010e\u0112\u0112\u0116\u0116\u0128"+
		"\u0128N\u0000\u0004\u0001\u0000\u0000\u0000\u0002\u000b\u0001\u0000\u0000"+
		"\u0000\u0004\u0005\u0005y\u0000\u0000\u0005\u0006\u0005\u0156\u0000\u0000"+
		"\u0006\u0007\u0005\u001b\u0000\u0000\u0007\b\u0005\b\u0000\u0000\b\t\u0006"+
		"\u0000\uffff\uffff\u0000\t\u0001\u0001\u0000\u0000\u0000\n\f\u0005F\u0000"+
		"\u0000\u000b\n\u0001\u0000\u0000\u0000\u000b\f\u0001\u0000\u0000\u0000"+
		"\f\u000e\u0001\u0000\u0000\u0000\r\u000f\u0007\u0000\u0000\u0000\u000e"+
		"\r\u0001\u0000\u0000\u0000\u000e\u000f\u0001\u0000\u0000\u0000\u000f\u0010"+
		"\u0001\u0000\u0000\u0000\u0010\u0011\u0005\u0085\u0000\u0000\u0011\u0015"+
		"\u0005\u0014\u0000\u0000\u0012\u0013\u0005\u0004\u0000\u0000\u0013\u0014"+
		"\u0005\u0014\u0000\u0000\u0014\u0016\u0005\u0005\u0000\u0000\u0015\u0012"+
		"\u0001\u0000\u0000\u0000\u0015\u0016\u0001\u0000\u0000\u0000\u0016\u0017"+
		"\u0001\u0000\u0000\u0000\u0017\u0018\u0005-\u0000\u0000\u0018\u0019\u0005"+
		"\u0018\u0000\u0000\u0019\u001a\u0005\u00c6\u0000\u0000\u001a\u001c\u0005"+
		"\u0018\u0000\u0000\u001b\u001d\u0005\u001f\u0000\u0000\u001c\u001b\u0001"+
		"\u0000\u0000\u0000\u001c\u001d\u0001\u0000\u0000\u0000\u001d$\u0001\u0000"+
		"\u0000\u0000\u001e\u001f\u0005\u00bd\u0000\u0000\u001f \u0005\u0094\u0000"+
		"\u0000 !\u0005\u0014\u0000\u0000!\"\u0005\u0012\u0000\u0000\"#\u0005\u0018"+
		"\u0000\u0000#%\u0005\u0013\u0000\u0000$\u001e\u0001\u0000\u0000\u0000"+
		"$%\u0001\u0000\u0000\u0000%&\u0001\u0000\u0000\u0000&9\u0005\u0001\u0000"+
		"\u0000\')\u0005u\u0000\u0000(*\u0005\u00c3\u0000\u0000)(\u0001\u0000\u0000"+
		"\u0000)*\u0001\u0000\u0000\u0000*+\u0001\u0000\u0000\u0000+3\u0005\u0014"+
		"\u0000\u0000,.\u0005\u0006\u0000\u0000-/\u0005\u00c3\u0000\u0000.-\u0001"+
		"\u0000\u0000\u0000./\u0001\u0000\u0000\u0000/0\u0001\u0000\u0000\u0000"+
		"02\u0005\u0014\u0000\u00001,\u0001\u0000\u0000\u000025\u0001\u0000\u0000"+
		"\u000031\u0001\u0000\u0000\u000034\u0001\u0000\u0000\u000046\u0001\u0000"+
		"\u0000\u000053\u0001\u0000\u0000\u000068\u0005\b\u0000\u00007\'\u0001"+
		"\u0000\u0000\u00008;\u0001\u0000\u0000\u000097\u0001\u0000\u0000\u0000"+
		"9:\u0001\u0000\u0000\u0000:?\u0001\u0000\u0000\u0000;9\u0001\u0000\u0000"+
		"\u0000<>\u0007\u0001\u0000\u0000=<\u0001\u0000\u0000\u0000>A\u0001\u0000"+
		"\u0000\u0000?=\u0001\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000@B\u0001"+
		"\u0000\u0000\u0000A?\u0001\u0000\u0000\u0000BC\u0005Y\u0000\u0000CD\u0005"+
		"\u0014\u0000\u0000DE\u0005\r\u0000\u0000E\u0003\u0001\u0000\u0000\u0000"+
		"\n\u000b\u000e\u0015\u001c$).39?";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}