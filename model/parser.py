from interlis_antlr_parser.grammar.generated.InterlisParserVisitor import InterlisParserVisitor
from model.core import Model, Topic, Class, DocText
from model.attributes import Attribute
from model.types import TextType, NumericType, EnumerationType, DomainType

class Parser(InterlisParserVisitor):
    def __init__(self):
        super().__init__()
        self.model = None

    def visitInterlis2def(self, ctx):
        self.models = []
        modeldefs = []
        if hasattr(ctx, 'modeldef'):
            md = ctx.modeldef()
            if isinstance(md, list):
                modeldefs = md
            elif md is not None:
                modeldefs = [md]
        for model_ctx in modeldefs:
            model = self.visit(model_ctx)
            if model:
                self.models.append(model)
        if self.models:
            self.model = self.models[0]
        return self.model

    def visitModeldef(self, ctx):
        name = "Unknown"
        contracted = False
        kind = ""
        language = ""
        at_value = ""
        version = ""
        no_incremental_transfer = False
        charset_iana_name = ""
        xmlns = ""
        submodels = []
        for i, child in enumerate(ctx.children):
            t = getattr(child, 'getText', lambda: None)()
            if t == 'CONTRACTED':
                contracted = True
            if t in ('TYPE', 'REFSYSTEM', 'SYMBOLOGY'):
                kind = t
            if t == 'MODEL' and i+1 < len(ctx.children):
                next_child = ctx.children[i+1]
                name = getattr(next_child, 'getText', lambda: None)()
            if t == '(' and i+1 < len(ctx.children):
                language = getattr(ctx.children[i+1], 'getText', lambda: None)()
            if t == 'AT' and i+1 < len(ctx.children):
                at_token = ctx.children[i+1]
                at_value = getattr(at_token, 'getText', lambda: None)()
                if at_value:
                    at_value = at_value.strip('"')
            if t == 'VERSION' and i+1 < len(ctx.children):
                version_token = ctx.children[i+1]
                version = getattr(version_token, 'getText', lambda: None)()
                if version:
                    version = version.strip('"')
            if t == 'NoIncrementalTransfer':
                no_incremental_transfer = True
            if t == 'CharSetIANAName' and i+1 < len(ctx.children):
                charset_iana_name = getattr(ctx.children[i+1], 'getText', lambda: None)()
                if charset_iana_name:
                    charset_iana_name = charset_iana_name.strip('"')
            if t == 'xmlns' and i+1 < len(ctx.children):
                xmlns = getattr(ctx.children[i+1], 'getText', lambda: None)()
                if xmlns:
                    xmlns = xmlns.strip('"')
        documentation = [DocText(name="Description", text="Importé via visitor")]
        topics = []
        from interlis_antlr_parser.grammar.generated.InterlisParser import InterlisParser
        for child in ctx.children:
            if type(child).__name__ == 'TopicDefContext':
                topic = self.visit(child)
                if topic:
                    topics.append(topic)
        model = Model(
            name=name,
            documentation=documentation,
            ili_version="2.4",
            contracted=contracted,
            kind=kind,
            language=language,
            at=at_value,
            version=version,
            no_incremental_transfer=no_incremental_transfer,
            charset_iana_name=charset_iana_name,
            xmlns=xmlns,
            submodels=submodels,
        )
        model.topics = topics
        return model

    def visitTopicDef(self, ctx):
        name = "UnknownTopic"
        if len(ctx.children) > 1:
            child1 = ctx.children[1]
            if hasattr(child1, 'getText'):
                name = child1.getText()
        classes = []
        for child in ctx.children:
            if hasattr(child, 'classDef'):
                class_defs = child.classDef()
                if class_defs is None:
                    continue
                if isinstance(class_defs, list):
                    defs = class_defs
                else:
                    defs = [class_defs]
                for class_ctx in defs:
                    cls = self.visit(class_ctx)
                    if cls:
                        classes.append(cls)
        topic = Topic(name=name, classes=classes)
        return topic

    def visitClassDef(self, ctx):
        name = "UnknownClass"
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
        else:
            for child in ctx.children:
                if hasattr(child, 'getText'):
                    text = child.getText()
                    if text not in ("CLASS", "STRUCTURE", "ASSOCIATION") and text.isidentifier():
                        name = text
                        break
        kind = "Class"
        attributes = []
        for child in ctx.children:
            if type(child).__name__ == 'ClassOrStructureDefContext':
                for sub in child.children:
                    if type(sub).__name__ == 'AttributeDefContext':
                        attr = self.visit(sub)
                        if attr:
                            attributes.append(attr)
        cls = Class(name=name, kind=kind, attributes=attributes)
        return cls

    def visitDomainDef(self, ctx):
        name = "UnknownDomain"
        if len(ctx.children) > 1:
            child1 = ctx.children[1]
            if hasattr(child1, 'getText'):
                name = child1.getText()
        type_ = None
        for child in ctx.children:
            if hasattr(child, 'type'):
                type_ctx = child.type()
                if type_ctx:
                    type_ = self.visit(type_ctx)
        domain = DomainType(name=name) if type_ is None else type_
        return domain

    def visitAttributeDef(self, ctx):
        name = "UnknownAttr"
        value = None
        mandatory = False
        
        # Extract attribute name
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
        else:
            for child in ctx.children:
                if hasattr(child, 'getText'):
                    text = child.getText()
                    if text.isidentifier() and text.isascii():
                        name = text
                        break
        
        # Check for MANDATORY keyword and extract type
        type_ = None
        if hasattr(ctx, 'attrTypeDef') and ctx.attrTypeDef():
            type_ctx = ctx.attrTypeDef()
            # Check if MANDATORY appears before the type
            for child in type_ctx.children:
                if hasattr(child, 'getText') and child.getText() == 'MANDATORY':
                    mandatory = True
            type_ = self.visit(type_ctx)
        else:
            type_ = TextType(name="TEXT", kind="TEXT")
        if name == "At":
            idx_name = None
            for i, child in enumerate(ctx.children):
                t = getattr(child, 'getText', lambda: None)()
                if t == name:
                    idx_name = i
                    break
            if idx_name is not None:
                for j in range(idx_name+1, len(ctx.children)):
                    t = getattr(ctx.children[j], 'getText', lambda: None)()
                    if t == ':':
                        for k in range(j+1, len(ctx.children)):
                            val = getattr(ctx.children[k], 'getText', lambda: None)()
                            if val and val not in (':', ';'):
                                value = val.strip('"')
                                break
                        break
        attr = Attribute(name=name, type_=type_, mandatory=mandatory)
        if value is not None:
            try:
                from model.attributes import MetaAttribute
                attr = MetaAttribute(name=name, value=value, type_=type_)
            except ImportError:
                attr.value = value
        return attr

    def visitAttrTypeDef(self, ctx):
        # Check children directly for numeric context
        for child in ctx.children:
            child_type = type(child).__name__
            if 'Numeric' in child_type:
                return self.visitNumericType(child)
            if 'Text' in child_type or child_type == 'AttrTypeContext':
                if hasattr(child, 'getText') and child.getText() == 'TEXT':
                    return self.visitTextType(child)
            if 'Enumeration' in child_type:
                return self.visitEnumerationType(child)
        
        # Fallback to attribute methods
        if hasattr(ctx, 'textType') and ctx.textType():
            return self.visit(ctx.textType())
        if hasattr(ctx, 'numericType') and ctx.numericType():
            return self.visit(ctx.numericType())
        if hasattr(ctx, 'enumerationType') and ctx.enumerationType():
            return self.visit(ctx.enumerationType())
        if hasattr(ctx, 'domainRef') and ctx.domainRef():
            return self.visit(ctx.domainRef())
        return TextType(name="TEXT", kind="TEXT")

    def visitTextType(self, ctx):
        return TextType(name="TEXT", kind="TEXT")

    def visitNumericType(self, ctx):
        min_val = None
        max_val = None
        
        # Parse numeric range: 0 .. 9999
        tokens = []
        for child in ctx.children:
            if hasattr(child, 'getText'):
                text = child.getText()
                if text not in ('MANDATORY',):
                    tokens.append(text)
        
        # Look for range pattern: min .. max
        for i, token in enumerate(tokens):
            if token == '..' and i > 0 and i < len(tokens) - 1:
                try:
                    min_val = tokens[i-1]
                    max_val = tokens[i+1]
                except (IndexError, ValueError):
                    pass
                break
        
        return NumericType(name="NUMERIC", min_value=min_val, max_value=max_val)

    def visitEnumerationType(self, ctx):
        values = []
        for child in ctx.children:
            if hasattr(child, 'getText'):
                val = child.getText()
                if val not in ("ENUMERATION", "END", ","):
                    values.append(val)
        return EnumerationType(name="ENUMERATION", values=values)

    def visitDomainRef(self, ctx):
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        return "UnknownDomainRef"


def parse_ili_model(ili_file_path: str):
    """
    Parse an INTERLIS model file and return the Model object.
    
    Args:
        ili_file_path: Path to the .ili file
        
    Returns:
        Model object representing the parsed INTERLIS model
    """
    from pathlib import Path
    path = Path(ili_file_path)
    if not path.exists():
        raise FileNotFoundError(f"ILI file not found: {ili_file_path}")
    ili_text = path.read_text(encoding="utf-8", errors="replace")
    return _parse_ili_text(ili_text)


def _parse_ili_text(ili_text: str):
    """Parse INTERLIS model text and return the Model object."""
    from antlr4 import InputStream, CommonTokenStream
    from interlis_antlr_parser.grammar.generated.InterlisLexer import InterlisLexer
    from interlis_antlr_parser.grammar.generated.InterlisParser import InterlisParser

    input_stream = InputStream(ili_text)
    lexer = InterlisLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = InterlisParser(stream)
    tree = parser.interlis2def()

    visitor = Parser()
    result = visitor.visit(tree)
    # If multiple models are found, return them all
    if hasattr(visitor, 'models') and visitor.models:
        return visitor.models
    return result


def parse_ili_model_text(ili_text: str):
    """Parse INTERLIS model text from a string."""
    return _parse_ili_text(ili_text)
