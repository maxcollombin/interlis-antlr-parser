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
		EQ=1, Scaling=2, LPAR=3, RPAR=4, COMMA=5, SEMI=6, LT=7, LTEQ=8, GT=9, 
		GTEQ=10, DOT=11, COLON=12, MINUS=13, PLUS=14, LCBR=15, RCBR=16, LSBR=17, 
		RSBR=18, Name=19, Letter=20, Digit=21, HexDigit=22, String=23, PosNumber=24, 
		Number=25, Dec=26, Float=27, Property=28, PropertyKeyword=29, Explanation=30, 
		ABSTRACT=31, ACCORDING=32, AGGREGATES=33, AGGREGATION=34, ALL=35, AND=36, 
		ANY=37, ANYCLASS=38, ANYSTRUCTURE=39, ARCS=40, AREA=41, AS=42, ASSOCIATION=43, 
		AT=44, ATTRIBUTE=45, ATTRIBUTES=46, BAG=47, BASE=48, BASED=49, BASKET=50, 
		BINARY=51, BLACKBOX=52, BLANK=53, BOOLEAN=54, BY=55, CARDINALITY=56, CHARSET=57, 
		CIRCULAR=58, CLASS=59, CLOCKWISE=60, CODE=61, CONSTRAINT=62, CONSTRAINTS=63, 
		CONTEXT=64, CONTINUE=65, CONTINUOUS=66, CONTOUR=67, CONTRACTED=68, COORD=69, 
		COORD2=70, COORD3=71, COUNTERCLOCKWISE=72, DATE=73, DATETIME=74, DEFAULT=75, 
		DEFERRED=76, DEFINED=77, DEGREES=78, DEPENDS=79, DERIVATIVES=80, DERIVED=81, 
		DIM1=82, DIM2=83, DIRECTED=84, DOMAIN=85, END=86, ENUM=87, ENUMTREEVAL=88, 
		ENUMVAL=89, EQUAL=90, EXISTENCE=91, EXTENDED=92, EXTENDS=93, EXTERNAL=94, 
		FINAL=95, FIRST=96, FIX=97, FONT=98, FORM=99, FORMAT=100, FREE=101, FROM=102, 
		FUNCTION=103, GENERIC=104, GENERICS=105, GRADS=106, GRAPHIC=107, HALIGNMENT=108, 
		HIDING=109, I16=110, I32=111, IDENT=112, IMPORTS=113, IN=114, INHERITANCE=115, 
		INSPECTION=116, INTERLIS=117, JOIN=118, LAST=119, LINE=120, LINEATTR=121, 
		LINESIZE=122, LIST=123, LNBASE=124, LOCAL=125, MANDATORY=126, METAOBJECT=127, 
		MODEL=128, MTEXT=129, MULTIAREA=130, MULTICOORD=131, MULTIPOLYLINE=132, 
		MULTISURFACE=133, NAME=134, NO=135, NOINCREMENTALTRANSFER=136, NOT=137, 
		NULL=138, NUMERIC=139, OBJECT=140, OBJECTS=141, OF=142, OID=143, ON=144, 
		OPTIONAL=145, OR=146, ORDERED=147, OTHERS=148, OVERLAPS=149, PARAMETER=150, 
		PARENT=151, PERIPHERY=152, PI=153, POLYLINE=154, PROJECTION=155, RADIANS=156, 
		REFERENCE=157, REFSYS=158, REFSYSTEM=159, REQUIRED=160, RESTRICTION=161, 
		ROTATION=162, SET=163, SIGN=164, STRAIGHTS=165, STRUCTURE=166, SUBDIVISION=167, 
		SURFACE=168, SYMBOLOGY=169, TABLE=170, TEXT=171, THATAREA=172, THIS=173, 
		THISAREA=174, TID=175, TIDSIZE=176, TIMEOFDAY=177, TO=178, TOPIC=179, 
		TRANSFER=180, TRANSIENT=181, TRANSLATION=182, TYPE=183, UNDEFINED=184, 
		UNION=185, UNIQUE=186, UNIT=187, UNQUALIFIED=188, URI=189, VALIGNMENT=190, 
		VERSION=191, VERTEX=192, VERTEXINFO=193, VIEW=194, WHEN=195, WHERE=196, 
		WITH=197, WITHOUT=198, XML=199, XMLNS=200, SingleLineComment=201, BlockComment=202, 
		TopicDef=203, Definitions=204, TopicRef=205, ClassDef=206, StructureDef=207, 
		ClassRef=208, ClassOrStructureDef=209, StructureRef=210, ClassOrStructureRef=211, 
		AttributeDef=212, AttrTypeDef=213, AttrType=214, ReferenceAttr=215, RestrictedClassOrAssRef=216, 
		ClassOrAssociationRef=217, RestrictedStructureRef=218, RestrictedClassOrStructureRef=219, 
		AssociationDef=220, AssociationRef=221, RoleDef=222, Cardinality=223, 
		DomainDef=224, Type=225, DomainRef=226, BaseType=227, Constant=228, TextType=229, 
		TextConst=230, EnumerationType=231, EnumTreeValueType=232, Enumeration=233, 
		EnumElement=234, EnumerationConst=235, AlignmentType=236, BooleanType=237, 
		NumericType=238, RefSys=239, DecConst=240, NumericConst=241, FormattedType=242, 
		FormatDef=243, BaseAttrRef=244, FormattedConst=245, DateTimeType=246, 
		CoordinateType=247, RotationDef=248, NullAxisPosNumber=249, PiHalfAxisPosNumber=250, 
		ContextDef=251, OIDType=252, BlackboxType=253, ClassType=254, AttributeType=255, 
		ClassConst=256, AttributePathConst=257, LineType=258, LineFormType=259, 
		ControlPoints=260, IntersectionDef=261, LineFormTypeDef=262, UnitDef=263, 
		DerivedUnit=264, ComposedUnit=265, UnitRef=266, MetaDataBasketDef=267, 
		MetaDataBasketRef=268, MetaObjectRef=269, ParameterDef=270, RunTimeParameterDef=271, 
		ConstraintDef=272, MandatoryConstraint=273, PlausibilityConstraint=274, 
		ExistenceConstraint=275, UniquenessConstraint=276, GlobalUniqueness=277, 
		UniqueEl=278, LocalUniqueness=279, SetConstraint=280, ConstraintsDef=281, 
		Expression=282, Term=283, Term0=284, Term1=285, Term2=286, Predicate=287, 
		Relation=288, FunctionDef=289, ArgumentDef=290, ArgumentType=291, ViewDef=292, 
		ViewRef=293, FormationDef=294, Projection=295, Join=296, Union=297, Aggregation=298, 
		Inspection=299, RenamedViewableRef=300, ViewableRef=301, BaseExtensionDef=302, 
		Selection=303, ViewAttributes=304, GraphicDef=305, GraphicRef=306, DrawingRule=307, 
		CondSignParamAssignment=308, SignParamAssignment=309, EnumAssignment=310, 
		EnumRange=311, Factor=312, SubEnumeration=313, MinDec=314, MaxDec=315, 
		RefSysMetaObjectRef=316, AxisPosNumber=317, CoordDomainRef=318, FormattedTypeDomainRef=319, 
		MinString=320, MaxString=321, NonNumString=322, IntPosPosNumber=323, FormattedDomainRef=324, 
		GenericCoordDefDomainRef=325, ConcreteDomainRef=326, AttributePath=327, 
		LineAttrDef=328, LogicalExpression=329, PercentageDec=330, ObjectOrAttributePath=331, 
		SignClassRef=332, EnumAttributePath=333, LineForm=334, WS=335;
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
			null, "'='", null, "'('", "')'", "','", "';'", "'<'", "'<='", "'>'", 
			"'>='", "'.'", "':'", "'-'", "'+'", "'{'", "'}'", "'['", "']'", null, 
			null, null, null, null, null, null, null, null, null, "'Properties'", 
			null, "'ABSTRACT'", "'ACCORDING'", "'AGGREGATES'", "'AGGREGATION'", "'ALL'", 
			"'AND'", "'ANY'", "'ANYCLASS'", "'ANYSTRUCTURE'", "'ARCS'", "'AREA'", 
			"'AS'", "'ASSOCIATION'", "'AT'", "'ATTRIBUTE'", "'ATTRIBUTES'", "'BAG'", 
			"'BASE'", "'BASED'", "'BASKET'", "'BINARY'", "'BLACKBOX'", "'BLANK'", 
			"'BOOLEAN'", "'BY'", "'CARDINALITY'", "'CHARSET'", "'CIRCULAR'", "'CLASS'", 
			"'CLOCKWISE'", "'CODE'", "'CONSTRAINT'", "'CONSTRAINTS'", "'CONTEXT'", 
			"'CONTINUE'", "'CONTINUOUS'", "'CONTOUR'", "'CONTRACTED'", "'COORD'", 
			"'COORD2'", "'COORD3'", "'COUNTERCLOCKWISE'", "'DATE'", "'DATETIME'", 
			"'DEFAULT'", "'DEFERRED'", "'DEFINED'", "'DEGREES'", "'DEPENDS'", "'DERIVATIVES'", 
			"'DERIVED'", "'DIM1'", "'DIM2'", "'DIRECTED'", "'DOMAIN'", "'END'", "'ENUM'", 
			"'ENUMTREEVAL'", "'ENUMVAL'", "'EQUAL'", "'EXISTENCE'", "'EXTENDED'", 
			"'EXTENDS'", "'EXTERNAL'", "'FINAL'", "'FIRST'", "'FIX'", "'FONT'", "'FORM'", 
			"'FORMAT'", "'FREE'", "'FROM'", "'FUNCTION'", "'GENERIC'", "'GENERICS'", 
			"'GRADS'", "'GRAPHIC'", "'HALIGNMENT'", "'HIDING'", "'I16'", "'I32'", 
			"'IDENT'", "'IMPORTS'", "'IN'", "'INHERITANCE'", "'INSPECTION'", "'INTERLIS'", 
			"'JOIN'", "'LAST'", "'LINE'", "'LINEATTR'", "'LINESIZE'", "'LIST'", "'LNBASE'", 
			"'LOCAL'", "'MANDATORY'", "'METAOBJECT'", "'MODEL'", "'MTEXT'", "'MULTIAREA'", 
			"'MULTICOORD'", "'MULTIPOLYLINE'", "'MULTISURFACE'", "'NAME'", "'NO'", 
			"'NOINCREMENTALTRANSFER'", "'NOT'", "'NULL'", "'NUMERIC'", "'OBJECT'", 
			"'OBJECTS'", "'OF'", "'OID'", "'ON'", "'OPTIONAL'", "'OR'", "'ORDERED'", 
			"'OTHERS'", "'OVERLAPS'", "'PARAMETER'", "'PARENT'", "'PERIPHERY'", "'PI'", 
			"'POLYLINE'", "'PROJECTION'", "'RADIANS'", "'REFERENCE'", "'REFSYS'", 
			"'REFSYSTEM'", "'REQUIRED'", "'RESTRICTION'", "'ROTATION'", "'SET'", 
			"'SIGN'", "'STRAIGHTS'", "'STRUCTURE'", "'SUBDIVISION'", "'SURFACE'", 
			"'SYMBOLOGY'", "'TABLE'", "'TEXT'", "'THATAREA'", "'THIS'", "'THISAREA'", 
			"'TID'", "'TIDSIZE'", "'TIMEOFDAY'", "'TO'", "'TOPIC'", "'TRANSFER'", 
			"'TRANSIENT'", "'TRANSLATION'", "'TYPE'", "'UNDEFINED'", "'UNION'", "'UNIQUE'", 
			"'UNIT'", "'UNQUALIFIED'", "'URI'", "'VALIGNMENT'", "'VERSION'", "'VERTEX'", 
			"'VERTEXINFO'", "'VIEW'", "'WHEN'", "'WHERE'", "'WITH'", "'WITHOUT'", 
			"'XML'", "'XMLNS'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "EQ", "Scaling", "LPAR", "RPAR", "COMMA", "SEMI", "LT", "LTEQ", 
			"GT", "GTEQ", "DOT", "COLON", "MINUS", "PLUS", "LCBR", "RCBR", "LSBR", 
			"RSBR", "Name", "Letter", "Digit", "HexDigit", "String", "PosNumber", 
			"Number", "Dec", "Float", "Property", "PropertyKeyword", "Explanation", 
			"ABSTRACT", "ACCORDING", "AGGREGATES", "AGGREGATION", "ALL", "AND", "ANY", 
			"ANYCLASS", "ANYSTRUCTURE", "ARCS", "AREA", "AS", "ASSOCIATION", "AT", 
			"ATTRIBUTE", "ATTRIBUTES", "BAG", "BASE", "BASED", "BASKET", "BINARY", 
			"BLACKBOX", "BLANK", "BOOLEAN", "BY", "CARDINALITY", "CHARSET", "CIRCULAR", 
			"CLASS", "CLOCKWISE", "CODE", "CONSTRAINT", "CONSTRAINTS", "CONTEXT", 
			"CONTINUE", "CONTINUOUS", "CONTOUR", "CONTRACTED", "COORD", "COORD2", 
			"COORD3", "COUNTERCLOCKWISE", "DATE", "DATETIME", "DEFAULT", "DEFERRED", 
			"DEFINED", "DEGREES", "DEPENDS", "DERIVATIVES", "DERIVED", "DIM1", "DIM2", 
			"DIRECTED", "DOMAIN", "END", "ENUM", "ENUMTREEVAL", "ENUMVAL", "EQUAL", 
			"EXISTENCE", "EXTENDED", "EXTENDS", "EXTERNAL", "FINAL", "FIRST", "FIX", 
			"FONT", "FORM", "FORMAT", "FREE", "FROM", "FUNCTION", "GENERIC", "GENERICS", 
			"GRADS", "GRAPHIC", "HALIGNMENT", "HIDING", "I16", "I32", "IDENT", "IMPORTS", 
			"IN", "INHERITANCE", "INSPECTION", "INTERLIS", "JOIN", "LAST", "LINE", 
			"LINEATTR", "LINESIZE", "LIST", "LNBASE", "LOCAL", "MANDATORY", "METAOBJECT", 
			"MODEL", "MTEXT", "MULTIAREA", "MULTICOORD", "MULTIPOLYLINE", "MULTISURFACE", 
			"NAME", "NO", "NOINCREMENTALTRANSFER", "NOT", "NULL", "NUMERIC", "OBJECT", 
			"OBJECTS", "OF", "OID", "ON", "OPTIONAL", "OR", "ORDERED", "OTHERS", 
			"OVERLAPS", "PARAMETER", "PARENT", "PERIPHERY", "PI", "POLYLINE", "PROJECTION", 
			"RADIANS", "REFERENCE", "REFSYS", "REFSYSTEM", "REQUIRED", "RESTRICTION", 
			"ROTATION", "SET", "SIGN", "STRAIGHTS", "STRUCTURE", "SUBDIVISION", "SURFACE", 
			"SYMBOLOGY", "TABLE", "TEXT", "THATAREA", "THIS", "THISAREA", "TID", 
			"TIDSIZE", "TIMEOFDAY", "TO", "TOPIC", "TRANSFER", "TRANSIENT", "TRANSLATION", 
			"TYPE", "UNDEFINED", "UNION", "UNIQUE", "UNIT", "UNQUALIFIED", "URI", 
			"VALIGNMENT", "VERSION", "VERTEX", "VERTEXINFO", "VIEW", "WHEN", "WHERE", 
			"WITH", "WITHOUT", "XML", "XMLNS", "SingleLineComment", "BlockComment", 
			"TopicDef", "Definitions", "TopicRef", "ClassDef", "StructureDef", "ClassRef", 
			"ClassOrStructureDef", "StructureRef", "ClassOrStructureRef", "AttributeDef", 
			"AttrTypeDef", "AttrType", "ReferenceAttr", "RestrictedClassOrAssRef", 
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
			if (((((_la - 159)) & ~0x3f) == 0 && ((1L << (_la - 159)) & 16778241L) != 0)) {
				{
				setState(13);
				_la = _input.LA(1);
				if ( !(((((_la - 159)) & ~0x3f) == 0 && ((1L << (_la - 159)) & 16778241L) != 0)) ) {
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
			while (((((_la - 203)) & ~0x3f) == 0 && ((1L << (_la - 203)) & 1729382256912367641L) != 0) || ((((_la - 267)) & ~0x3f) == 0 && ((1L << (_la - 267)) & 4194321L) != 0)) {
				{
				{
				setState(60);
				_la = _input.LA(1);
				if ( !(((((_la - 203)) & ~0x3f) == 0 && ((1L << (_la - 203)) & 1729382256912367641L) != 0) || ((((_la - 267)) & ~0x3f) == 0 && ((1L << (_la - 267)) & 4194321L) != 0)) ) {
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
		"\u0004\u0001\u014fG\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0001"+
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
		"\u0002\u0003\u0000\u009f\u009f\u00a9\u00a9\u00b7\u00b7\u0007\u0000\u00cb"+
		"\u00cb\u00ce\u00cf\u00e0\u00e0\u0106\u0107\u010b\u010b\u010f\u010f\u0121"+
		"\u0121N\u0000\u0004\u0001\u0000\u0000\u0000\u0002\u000b\u0001\u0000\u0000"+
		"\u0000\u0004\u0005\u0005u\u0000\u0000\u0005\u0006\u0005\u014f\u0000\u0000"+
		"\u0006\u0007\u0005\u001a\u0000\u0000\u0007\b\u0005\u0006\u0000\u0000\b"+
		"\t\u0006\u0000\uffff\uffff\u0000\t\u0001\u0001\u0000\u0000\u0000\n\f\u0005"+
		"D\u0000\u0000\u000b\n\u0001\u0000\u0000\u0000\u000b\f\u0001\u0000\u0000"+
		"\u0000\f\u000e\u0001\u0000\u0000\u0000\r\u000f\u0007\u0000\u0000\u0000"+
		"\u000e\r\u0001\u0000\u0000\u0000\u000e\u000f\u0001\u0000\u0000\u0000\u000f"+
		"\u0010\u0001\u0000\u0000\u0000\u0010\u0011\u0005\u0080\u0000\u0000\u0011"+
		"\u0015\u0005\u0013\u0000\u0000\u0012\u0013\u0005\u0003\u0000\u0000\u0013"+
		"\u0014\u0005\u0013\u0000\u0000\u0014\u0016\u0005\u0004\u0000\u0000\u0015"+
		"\u0012\u0001\u0000\u0000\u0000\u0015\u0016\u0001\u0000\u0000\u0000\u0016"+
		"\u0017\u0001\u0000\u0000\u0000\u0017\u0018\u0005,\u0000\u0000\u0018\u0019"+
		"\u0005\u0017\u0000\u0000\u0019\u001a\u0005\u00bf\u0000\u0000\u001a\u001c"+
		"\u0005\u0017\u0000\u0000\u001b\u001d\u0005\u001e\u0000\u0000\u001c\u001b"+
		"\u0001\u0000\u0000\u0000\u001c\u001d\u0001\u0000\u0000\u0000\u001d$\u0001"+
		"\u0000\u0000\u0000\u001e\u001f\u0005\u00b6\u0000\u0000\u001f \u0005\u008e"+
		"\u0000\u0000 !\u0005\u0013\u0000\u0000!\"\u0005\u0011\u0000\u0000\"#\u0005"+
		"\u0017\u0000\u0000#%\u0005\u0012\u0000\u0000$\u001e\u0001\u0000\u0000"+
		"\u0000$%\u0001\u0000\u0000\u0000%&\u0001\u0000\u0000\u0000&9\u0005\u0001"+
		"\u0000\u0000\')\u0005q\u0000\u0000(*\u0005\u00bc\u0000\u0000)(\u0001\u0000"+
		"\u0000\u0000)*\u0001\u0000\u0000\u0000*+\u0001\u0000\u0000\u0000+3\u0005"+
		"\u0013\u0000\u0000,.\u0005\u0005\u0000\u0000-/\u0005\u00bc\u0000\u0000"+
		".-\u0001\u0000\u0000\u0000./\u0001\u0000\u0000\u0000/0\u0001\u0000\u0000"+
		"\u000002\u0005\u0013\u0000\u00001,\u0001\u0000\u0000\u000025\u0001\u0000"+
		"\u0000\u000031\u0001\u0000\u0000\u000034\u0001\u0000\u0000\u000046\u0001"+
		"\u0000\u0000\u000053\u0001\u0000\u0000\u000068\u0005\u0006\u0000\u0000"+
		"7\'\u0001\u0000\u0000\u00008;\u0001\u0000\u0000\u000097\u0001\u0000\u0000"+
		"\u00009:\u0001\u0000\u0000\u0000:?\u0001\u0000\u0000\u0000;9\u0001\u0000"+
		"\u0000\u0000<>\u0007\u0001\u0000\u0000=<\u0001\u0000\u0000\u0000>A\u0001"+
		"\u0000\u0000\u0000?=\u0001\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000"+
		"@B\u0001\u0000\u0000\u0000A?\u0001\u0000\u0000\u0000BC\u0005V\u0000\u0000"+
		"CD\u0005\u0013\u0000\u0000DE\u0005\u000b\u0000\u0000E\u0003\u0001\u0000"+
		"\u0000\u0000\n\u000b\u000e\u0015\u001c$).39?";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}