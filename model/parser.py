from interlis_antlr_parser.grammar.generated.InterlisParserVisitor import InterlisParserVisitor
from model.core import Model, Topic, Class, DocText
from model.attributes import Attribute
from model.types import TextType, NumericType, EnumType, Type

class Parser(InterlisParserVisitor):
    def __init__(self):
        super().__init__()
        self.model = None

    def visitInterlis2def(self, ctx):
        print("[DEBUG] visitInterlis2def called")
        models = []
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
                models.append(model)
        if models:
            self.model = models[0]
        return self.model

    def visitModeldef(self, ctx):
        print("[DEBUG] visitModeldef called")
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
        print(f"[DEBUG] Model: {name}, contracted: {contracted}, kind: {kind}, language: {language}, at: {at_value}, version: {version}, topics: {len(topics)}")
        return model

    def visitTopicDef(self, ctx):
        print("[DEBUG] visitTopicDef called")
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
        print(f"[DEBUG] Topic: {name}, classes: {len(classes)}")
        return topic

    def visitClassDef(self, ctx):
        print("[DEBUG] visitClassDef called")
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
        print(f"[DEBUG] Class: {name}, attributes: {len(attributes)}")
        return cls

    def visitDomainDef(self, ctx):
        print("[DEBUG] visitDomainDef called")
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
        from model.types import Type
        domain = Type() if type_ is None else type_
        print(f"[DEBUG] Domain: {name}, type: {type_}")
        return domain

    def visitAttributeDef(self, ctx):
        print("[DEBUG] visitAttributeDef called (typed)")
        print("[DEBUG]   Children of AttributeDefContext:")
        for i, child in enumerate(ctx.children):
            t = getattr(child, 'getText', lambda: None)()
            print(f"    [{i}] {type(child).__name__}: '{t}'")
        name = "UnknownAttr"
        value = None
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            name = ctx.IDENTIFIER().getText()
        else:
            for child in ctx.children:
                if hasattr(child, 'getText'):
                    text = child.getText()
                    if text.isidentifier() and text.isascii():
                        name = text
                        break
        type_ = None
        if hasattr(ctx, 'attrTypeDef') and ctx.attrTypeDef():
            type_ = self.visit(ctx.attrTypeDef())
        else:
            type_ = TextType(kind="TEXT")
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
        print(f"[DEBUG]   Attribut extrait: {name}, type: {type(type_).__name__ if type_ else 'None'}, value: {value}")
        attr = Attribute(name=name, type_=type_)
        if value is not None:
            try:
                from model.attributes import MetaAttribute
                attr = MetaAttribute(name=name, value=value, type_=type_)
            except ImportError:
                attr.value = value
        return attr

    def visitAttrTypeDef(self, ctx):
        if hasattr(ctx, 'textType') and ctx.textType():
            return self.visit(ctx.textType())
        if hasattr(ctx, 'numericType') and ctx.numericType():
            return self.visit(ctx.numericType())
        if hasattr(ctx, 'enumerationType') and ctx.enumerationType():
            return self.visit(ctx.enumerationType())
        if hasattr(ctx, 'domainRef') and ctx.domainRef():
            return self.visit(ctx.domainRef())
        return TextType(kind="TEXT")

    def visitTextType(self, ctx):
        print("[DEBUG] visitTextType called")
        return TextType(kind="TEXT")

    def visitNumericType(self, ctx):
        print("[DEBUG] visitNumericType called")
        return NumericType()

    def visitEnumerationType(self, ctx):
        print("[DEBUG] visitEnumerationType called")
        values = []
        for child in ctx.children:
            if hasattr(child, 'getText'):
                val = child.getText()
                if val not in ("ENUMERATION", "END", ","):
                    values.append(val)
        return EnumType(values=values)

    def visitDomainRef(self, ctx):
        print("[DEBUG] visitDomainRef called")
        if hasattr(ctx, 'IDENTIFIER') and ctx.IDENTIFIER():
            return ctx.IDENTIFIER().getText()
        return "UnknownDomainRef"
