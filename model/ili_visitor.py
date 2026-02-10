"""
Visitor ANTLR pour INTERLIS 2.4.

Responsabilité : construire l'AST enrichi uniquement.
La résolution sémantique se fait dans IliResolver (phase séparée).

Étapes d'extraction :
1. MODEL : nom, version, language, at
2. DOMAIN (globaux)
3. TOPIC : nom, domaines locaux
4. CLASS : nom, abstract, final, kind, attributs
5. ATTRIBUTE : nom, type, mandatory
"""

from interlis_antlr_parser.grammar.generated.InterlisParserVisitor import InterlisParserVisitor
from model.metamodel import (
    IliModel, IliTopic, IliClass, IliDomain, IliAttribute, IliDocumentation,
    IliType, IliCardinality, IliAssociation, IliRole, IliGeometry
)
from model.expressions import (
    Expression, Factor, PathFactor, ConstantFactor, UnitRefFactor, 
    EnumMappingFactor, Literal
)


class IliVisitor(InterlisParserVisitor):
    """Construit un IliModel à partir de l'AST ANTLR."""
    
    def __init__(self, debug: bool = True):
        super().__init__()
        self.model = None
        self.debug = debug
    
    def _log(self, msg: str, level: str = "INFO"):
        """Log avec niveau."""
        if self.debug:
            prefix = f"[{level}]" if level else ""
            print(f"{prefix} {msg}")
    
    def visitInterlis2def(self, ctx):
        """Entrée principale (INTERLIS 2.4; ... MODEL ...)."""
        self._log("visitInterlis2def")
        
        # Étape 0 : Extraire la version INTERLIS globale (ex: INTERLIS 2.4;)
        interlis_version = self._extract_interlis_version(ctx)
        self._log(f"  INTERLIS version: {interlis_version}", "STEP0")
        
        # Étape 1 : Extraire les modèles
        models = []
        
        if hasattr(ctx, 'modeldef'):
            modeldefs = ctx.modeldef()
            if modeldefs:
                if isinstance(modeldefs, list):
                    models = [self.visit(md) for md in modeldefs if self.visit(md)]
                else:
                    model = self.visit(modeldefs)
                    if model:
                        models = [model]
        
        if models:
            self.model = models[0]
            # Mettre à jour la version INTERLIS du modèle
            if interlis_version:
                self.model.ili_version = interlis_version
        
        return self.model
    
    def visitModeldef(self, ctx):
        """Visite la définition d'un modèle (MODEL IlisMeta16 (en) AT ...)."""
        self._log("visitModeldef")
        
        # Étape 1 : Extraire le nom du modèle (MODEL <name>)
        model_name = self._extract_model_name(ctx)
        self._log(f"  Model name: {model_name}", "STEP1")
        
        if not model_name or model_name == "Unknown":
            self._log(f"  ❌ Failed to extract model name", "ERROR")
            return None
        
        # Étape 2 : Extraire les propriétés (VERSION, AT, LANGUAGE, etc.)
        version = self._extract_string_after_keyword(ctx, "VERSION")
        at = self._extract_string_after_keyword(ctx, "AT")
        language = self._extract_language(ctx)
        contracted = self._has_keyword(ctx, "CONTRACTED")
        
        self._log(f"  Version: {version}", "STEP1")
        self._log(f"  AT: {at}", "STEP1")
        self._log(f"  Language: {language}", "STEP1")
        self._log(f"  Contracted: {contracted}", "STEP1")
        
        # Créer le modèle
        model = IliModel(
            name=model_name,
            ili_version="2.4",  # Sera complété par visitInterlis2def
            version=version if version else None,
            at=at if at else None,
            language=language if language else None,
            contracted=contracted,
        )
        
        # Étape 3 : Extraire les domaines globaux (avant les TOPIC)
        self._log("  Extracting global domains...", "STEP2")
        global_domains = self._extract_global_domains(ctx)
        for domain in global_domains:
            model.topics  # TODO: store in model if needed
        
        # Étape 4 : Extraire les TOPICs
        self._log("  Extracting topics...", "STEP3")
        topics = self._extract_topics(ctx)
        
        for topic in topics:
            model.topics[topic.name] = topic
        
        self._log(f"  ✓ Model '{model_name}': {len(model.topics)} topics", "SUCCESS")
        return model
    
    def visitTopicDef(self, ctx):
        """Visite TOPIC ... ="""
        topic_name = self._extract_identifier_after_keyword(ctx, "TOPIC")
        self._log(f"visitTopicDef: {topic_name}")
        
        topic = IliTopic(
            name=topic_name,
            ili_name=topic_name,
        )
        
        # Extraire les éléments du topic (classes, domaines, associations)
        self._extract_topic_contents(ctx, topic)
        
        self._log(f"  ✓ Topic '{topic_name}': {len(topic.classes)} classes, {len(topic.domains)} domains")
        return topic
    
    def visitClassDef(self, ctx):
        """Visite CLASS ... ="""
        class_name = self._extract_identifier_after_keyword(ctx, "CLASS")
        self._log(f"visitClassDef: {class_name}")
        
        # Déterminer les propriétés
        abstract = self._has_keyword(ctx, "ABSTRACT")
        final = self._has_keyword(ctx, "FINAL")
        
        cls = IliClass(
            name=class_name,
            ili_name=class_name,
            abstract=abstract,
            final=final,
        )
        
        # Extraire les attributs
        self._extract_class_attributes(ctx, cls)
        
        self._log(f"  ✓ Class '{class_name}' (abstract={abstract}): {len(cls.attributes)} attributes")
        return cls
    
    def visitAttributeDef(self, ctx):
        """Visite un attribut dans une classe."""
        attr_name = self._extract_first_identifier(ctx)
        
        # Déterminer le type et les propriétés
        type_ = IliType.TEXT  # Défaut
        mandatory = self._has_keyword(ctx, "MANDATORY")
        
        # Détecter les domaines référencés (ex: Kind: MANDATORY (...))
        domain_ref = self._extract_domain_reference(ctx, attr_name)
        
        attr = IliAttribute(
            name=attr_name,
            ili_name=attr_name,
            type_=type_,
            mandatory=mandatory,
        )
        
        self._log(f"  Attr: {attr_name} (mandatory={mandatory})", "ATTR")
        return attr
    
    def _extract_domain_reference(self, ctx, attr_name: str) -> str:
        """Extrait la référence de domaine pour un attribut."""
        # Chercher dans le contenu de l'attribut
        text = self._getText(ctx)
        if ":" in text:
            parts = text.split(":")
            if len(parts) > 1:
                type_part = parts[1].strip()
                # Extraire le nom du domaine/type
                words = type_part.split()
                for word in words:
                    if word and word not in ("MANDATORY", "OPTIONAL", "LIST", "OF", "BAG", ";"):
                        return word
        return ""
    
    def visitDomainDef(self, ctx):
        """Visite DOMAIN ... ="""
        domain_name = self._extract_identifier_after_keyword(ctx, "DOMAIN")
        self._log(f"visitDomainDef: {domain_name}")
        
        domain = IliDomain(
            name=domain_name,
            ili_name=domain_name,
            type_=IliType.TEXT,
        )
        
        return domain
    
    # ===== MÉTHODES UTILITAIRES D'EXTRACTION =====
    
    def _extract_interlis_version(self, ctx) -> str:
        """Extrait la version INTERLIS globale (INTERLIS 2.4;)."""
        text = self._getText(ctx)
        # Chercher "INTERLIS X.X" au début
        if "INTERLIS" in text:
            parts = text.split()
            for i, part in enumerate(parts):
                if part == "INTERLIS" and i + 1 < len(parts):
                    version = parts[i + 1].rstrip(";")
                    if version and ("." in version or version[0].isdigit()):
                        return version
        return "2.4"  # Défaut
    
    def _extract_model_name(self, ctx) -> str:
        """Extrait le nom du modèle (MODEL <name>)."""
        for i, child in enumerate(ctx.children):
            if self._getText(child) == "MODEL" and i + 1 < len(ctx.children):
                name = self._getText(ctx.children[i + 1])
                if name and name.isidentifier():
                    return name
        return "Unknown"
    
    def _extract_global_domains(self, ctx) -> list:
        """Extrait les domaines globaux du modèle (avant les TOPIC)."""
        domains = []
        # TODO: Implémentation future
        return domains
    
    def _extract_topics(self, ctx) -> list:
        """Extrait tous les TOPICs du modèle."""
        topics = []
        for child in ctx.children:
            if type(child).__name__ == "TopicDefContext":
                topic = self.visit(child)
                if topic:
                    topics.append(topic)
        return topics
    
    def _extract_topic_contents(self, ctx, topic: IliTopic):
        """Extrait les éléments d'un TOPIC (classes, domaines, etc.)."""
        for child in ctx.children:
            child_type = type(child).__name__
            
            if child_type == "ClassDefContext":
                cls = self.visit(child)
                if cls:
                    topic.classes[cls.name] = cls
            
            elif child_type == "StructureDefContext":
                cls = self.visit(child)
                if cls:
                    topic.classes[cls.name] = cls
            
            # Visiter les conteneurs imbriqués
            elif hasattr(child, 'children'):
                for sub in child.children:
                    sub_type = type(sub).__name__
                    if sub_type == "ClassDefContext":
                        cls = self.visit(sub)
                        if cls:
                            topic.classes[cls.name] = cls
                    elif sub_type == "StructureDefContext":
                        cls = self.visit(sub)
                        if cls:
                            topic.classes[cls.name] = cls
    
    def _extract_class_attributes(self, ctx, cls: IliClass):
        """Extrait tous les attributs d'une classe."""
        for child in ctx.children:
            if type(child).__name__ == "AttributeDefContext":
                attr = self.visit(child)
                if attr:
                    cls.attributes[attr.name] = attr
            
            # Rechercher dans les conteneurs imbriqués
            elif hasattr(child, 'children'):
                for sub in child.children:
                    if type(sub).__name__ == "AttributeDefContext":
                        attr = self.visit(sub)
                        if attr:
                            cls.attributes[attr.name] = attr
    
    def _extract_identifier_after_keyword(self, ctx, keyword: str) -> str:
        """Extrait l'identifiant suivant un mot-clé (ex: TOPIC nom)."""
        for i, child in enumerate(ctx.children):
            if self._getText(child) == keyword and i + 1 < len(ctx.children):
                text = self._getText(ctx.children[i + 1])
                if text.isidentifier():
                    return text
        return "Unknown"
    
    def _extract_string_after_keyword(self, ctx, keyword: str) -> str:
        """Extrait une chaîne de caractères après un mot-clé."""
        for i, child in enumerate(ctx.children):
            if self._getText(child) == keyword and i + 1 < len(ctx.children):
                text = self._getText(ctx.children[i + 1])
                # Supprimer les guillemets
                if text.startswith('"') and text.endswith('"'):
                    return text[1:-1]
                return text
        return ""
    
    def _extract_language(self, ctx) -> str:
        """Extrait la langue (MODEL ... (en) ...)."""
        for i, child in enumerate(ctx.children):
            text = self._getText(child)
            if text == "(" and i + 1 < len(ctx.children):
                next_text = self._getText(ctx.children[i + 1])
                if next_text == ")":
                    continue
                # C'est probablement la langue
                if len(next_text) <= 5 and next_text.isalpha():
                    return next_text
        return ""
    
    def _extract_first_identifier(self, ctx) -> str:
        """Extrait le premier identifiant dans les children."""
        for child in ctx.children:
            text = self._getText(child)
            if text and text.isidentifier() and text not in ("MANDATORY", "OPTIONAL", "END"):
                return text
        return "Unknown"
    
    def _has_keyword(self, ctx, keyword: str) -> bool:
        """Vérifie si un mot-clé existe."""
        for child in ctx.children:
            if self._getText(child) == keyword:
                return True
        return False
    
    def _getText(self, node) -> str:
        """Récupère le texte d'un nœud."""
        if hasattr(node, 'getText'):
            return node.getText()
        return str(node) if node else ""
    
    # ===== HELPERS POUR EXPRESSIONS (ANTLR → CONCEPTUEL) =====
    
    def visitFactor(self, ctx) -> Factor:
        """
        Visite un facteur ANTLR et le convertit en facteur conceptuel.
        
        Mapping :
        - Constant → ConstantFactor (Literal)
        - ObjectOrAttributePath → PathFactor
        - UnitRef → UnitRefFactor
        - EnumMapping → EnumMappingFactor
        """
        # Cas 1 : Constante (nombre, texte, booléen)
        if hasattr(ctx, 'constant') and ctx.constant():
            return self._extract_constant_factor(ctx.constant())
        
        # Cas 2 : Chemin d'attribut/objet
        if hasattr(ctx, 'objectOrAttributePath') and ctx.objectOrAttributePath():
            path = self._extract_path(ctx.objectOrAttributePath())
            return PathFactor(path=path)
        
        # Cas 3 : Référence d'unité (rare, unités dérivées/composées)
        if hasattr(ctx, 'unitRef') and ctx.unitRef():
            unit_ref = self._getText(ctx.unitRef())
            return UnitRefFactor(unit_ref=unit_ref)
        
        # Cas 4 : Mapping d'énumération (graphique)
        if hasattr(ctx, 'enumMapping') and ctx.enumMapping():
            mapping = self._getText(ctx.enumMapping())
            return EnumMappingFactor(mapping=mapping)
        
        # Fallback : facteur générique
        return Factor()
    
    def _extract_constant_factor(self, ctx) -> ConstantFactor:
        """Extrait une constante et crée un ConstantFactor."""
        text = self._getText(ctx)
        
        # Déterminer le type de la constante
        literal_type = "TEXT"
        if text.isdigit() or (text.replace('.', '', 1).isdigit() and text.count('.') <= 1):
            literal_type = "NUMERIC"
        elif text.upper() in ("TRUE", "FALSE"):
            literal_type = "BOOLEAN"
        elif text.startswith('"') or text.startswith("'"):
            literal_type = "TEXT"
            text = text.strip('"').strip("'")  # Nettoyer les guillemets
        
        literal = Literal(value=text, literal_type=literal_type)
        return ConstantFactor(literal=literal)
    
    def _extract_path(self, ctx) -> str:
        """Extrait un chemin d'attribut (THIS.Name, Base.Id, etc.)."""
        return self._getText(ctx)
    
    def visitExpression(self, ctx) -> Expression:
        """
        Visite une expression ANTLR.
        
        Note : La structure syntaxique (UnaryExpr, CompoundExpr) reste dans ANTLR.
        On extrait uniquement les facteurs conceptuels (constantes, chemins, etc.).
        """
        # Si l'expression contient un facteur, on le retourne
        if hasattr(ctx, 'factor') and ctx.factor():
            factors = ctx.factor() if isinstance(ctx.factor(), list) else [ctx.factor()]
            if len(factors) == 1:
                return self.visitFactor(factors[0])
        
        # Pour les expressions complexes, on peut stocker le texte brut
        # (la résolution syntaxique reste dans ANTLR)
        return Expression()
