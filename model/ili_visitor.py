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
from model.constraints import (
    Constraint, MandatoryConstraint, PlausibilityConstraint,
    ExistenceConstraint, UniqueConstraint, SetConstraint,
    CardinalityConstraint, AreaConnectedConstraint, LineTopologyConstraint,
    GeometryConstraint, ConstraintSeverity, ConstraintScope
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
        
        # Extraire les contraintes au niveau de la classe
        self._extract_class_constraints(ctx, cls)
        
        self._log(f"  ✓ Class '{class_name}' (abstract={abstract}): {len(cls.attributes)} attributes, {len(cls.constraints)} constraints")
        return cls
    
    def visitAttributeDef(self, ctx):
        """Visite un attribut dans une classe (supporte types géométriques)."""
        attr_name = self._extract_first_identifier(ctx)
        mandatory = self._has_keyword(ctx, "MANDATORY")
        domain_ref = self._extract_domain_reference(ctx, attr_name)

        # Résoudre le type du domaine référencé (si connu)
        from model.types import CoordType, LineType, AreaType, SurfaceType, VertexType, LengthType, AngleType, TextType, NumericType, EnumerationType, DomainType
        type_lower = domain_ref.lower() if domain_ref else ""
        if "coord" in type_lower:
            type_ = CoordType(ili_name=domain_ref)
        elif "polyline" in type_lower or "line" in type_lower:
            type_ = LineType(ili_name=domain_ref)
        elif "area" in type_lower:
            type_ = AreaType(ili_name=domain_ref)
        elif "surface" in type_lower:
            type_ = SurfaceType(ili_name=domain_ref)
        elif "vertex" in type_lower:
            type_ = VertexType(ili_name=domain_ref)
        elif "length" in type_lower:
            type_ = LengthType(ili_name=domain_ref)
        elif "angle" in type_lower:
            type_ = AngleType(ili_name=domain_ref)
        elif "text" in type_lower:
            type_ = TextType(ili_name=domain_ref)
        elif "numeric" in type_lower or "number" in type_lower:
            type_ = NumericType(ili_name=domain_ref)
        elif "enum" in type_lower:
            type_ = EnumerationType(ili_name=domain_ref)
        elif domain_ref:
            type_ = DomainType(ili_name=domain_ref)
        else:
            type_ = DomainType(ili_name="TEXT")

        attr = IliAttribute(
            name=attr_name,
            ili_name=attr_name,
            type_=type_,
            mandatory=mandatory,
        )
        self._log(f"  Attr: {attr_name} (mandatory={mandatory}, type={type_})", "ATTR")
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
        """Visite DOMAIN ... = (supporte types géométriques)"""
        domain_name = self._extract_identifier_after_keyword(ctx, "DOMAIN")
        self._log(f"visitDomainDef: {domain_name}")

        # Extraire le type INTERLIS (ex: COORD, POLYLINE, AREA, SURFACE, etc.)
        type_text = self._getText(ctx)
        type_lower = type_text.lower()
        from model.types import CoordType, LineType, AreaType, SurfaceType, VertexType, LengthType, AngleType, TextType, NumericType, EnumerationType, DomainType

        # Heuristique simple pour détecter le type
        if "coord" in type_lower:
            domain_type = CoordType(ili_name=domain_name)
        elif "polyline" in type_lower or "line" in type_lower:
            domain_type = LineType(ili_name=domain_name)
        elif "area" in type_lower:
            domain_type = AreaType(ili_name=domain_name)
        elif "surface" in type_lower:
            domain_type = SurfaceType(ili_name=domain_name)
        elif "vertex" in type_lower:
            domain_type = VertexType(ili_name=domain_name)
        elif "length" in type_lower:
            domain_type = LengthType(ili_name=domain_name)
        elif "angle" in type_lower:
            domain_type = AngleType(ili_name=domain_name)
        elif "text" in type_lower:
            domain_type = TextType(ili_name=domain_name)
        elif "numeric" in type_lower or "number" in type_lower:
            domain_type = NumericType(ili_name=domain_name)
        elif "enum" in type_lower:
            domain_type = EnumerationType(ili_name=domain_name)
        else:
            domain_type = DomainType(ili_name=domain_name)

        domain = IliDomain(
            name=domain_name,
            ili_name=domain_name,
            type_=domain_type,
        )
        return domain
    
    # ===== CONTRAINTES INTERLIS =====
    
    def visitConstraintsDef(self, ctx):
        """Visite CONSTRAINTS OF ... = ... END;"""
        self._log("visitConstraintsDef")
        
        # Extraire la référence à la classe (classOrAssociationRef)
        applies_to = ""
        if hasattr(ctx, 'classOrAssociationRef') and ctx.classOrAssociationRef():
            applies_to = self._getText(ctx.classOrAssociationRef())
        
        self._log(f"  Constraints for: {applies_to}", "CONSTRAINT")
        
        # Extraire tous les constraintDef
        constraints = []
        if hasattr(ctx, 'constraintDef'):
            constraint_defs = ctx.constraintDef()
            if constraint_defs:
                if not isinstance(constraint_defs, list):
                    constraint_defs = [constraint_defs]
                
                for constraint_def in constraint_defs:
                    constraint = self.visitConstraintDef(constraint_def)
                    if constraint:
                        constraint.applies_to = applies_to
                        constraints.append(constraint)
        
        self._log(f"  ✓ Extracted {len(constraints)} constraints", "SUCCESS")
        return constraints
    
    def visitConstraintDef(self, ctx):
        """Visite une définition de contrainte (dispatcher)."""
        self._log("visitConstraintDef")
        
        # Déterminer le type de contrainte et dispatcher
        if hasattr(ctx, 'mandatoryConstraint') and ctx.mandatoryConstraint():
            return self.visitMandatoryConstraint(ctx.mandatoryConstraint())
        
        elif hasattr(ctx, 'plausibilityConstraint') and ctx.plausibilityConstraint():
            return self.visitPlausibilityConstraint(ctx.plausibilityConstraint())
        
        elif hasattr(ctx, 'existenceConstraint') and ctx.existenceConstraint():
            return self.visitExistenceConstraint(ctx.existenceConstraint())
        
        elif hasattr(ctx, 'uniquenessConstraint') and ctx.uniquenessConstraint():
            return self.visitUniquenessConstraint(ctx.uniquenessConstraint())
        
        elif hasattr(ctx, 'setConstraint') and ctx.setConstraint():
            return self.visitSetConstraint(ctx.setConstraint())
        
        self._log("  ⚠ Unknown constraint type", "WARNING")
        return None
    
    def visitMandatoryConstraint(self, ctx):
        """Visite MANDATORY CONSTRAINT"""
        self._log("  visitMandatoryConstraint", "CONSTRAINT")
        
        # Extraire le nom (optionnel: Name COLON avant l'expression)
        constraint_name = self._extract_optional_constraint_name(ctx)
        
        # L'expression est le premier expression() du contexte
        expression = None
        if hasattr(ctx, 'expression') and ctx.expression():
            expression = self.visitExpression(ctx.expression())
        
        constraint = MandatoryConstraint(
            name=constraint_name if constraint_name else "MandatoryConstraint",
            ili_name=constraint_name if constraint_name else "MandatoryConstraint",
            logical_expression=expression,
            scope=ConstraintScope.ATTRIBUTE,
        )
        
        self._log(f"    ✓ MandatoryConstraint: {constraint.ili_name}", "CONSTRAINT_OK")
        return constraint
    
    def visitPlausibilityConstraint(self, ctx):
        """Visite PLAUSIBILITY CONSTRAINT (CHECK ...)"""
        self._log("  visitPlausibilityConstraint", "CONSTRAINT")
        
        # Extraire le nom (optionnel)
        constraint_name = self._extract_optional_constraint_name(ctx)
        
        # Extraire le pourcentage et direction
        percentage = None
        direction = None
        
        if hasattr(ctx, 'numericConst') and ctx.numericConst():
            try:
                percentage = float(self._getText(ctx.numericConst()))
            except:
                pass
        
        # Vérifier les tokens pour direction (LTEQ, GTEQ)
        if hasattr(ctx, 'LTEQ') and ctx.LTEQ():
            direction = "<="
        elif hasattr(ctx, 'GTEQ') and ctx.GTEQ():
            direction = ">="
        
        # Extraire l'expression
        expression = None
        if hasattr(ctx, 'expression') and ctx.expression():
            expr_ctx = ctx.expression()
            if not isinstance(expr_ctx, list):
                expr_ctx = [expr_ctx]
            if expr_ctx:
                expression = self.visitExpression(expr_ctx[0])
        
        constraint = PlausibilityConstraint(
            name=constraint_name if constraint_name else "PlausibilityConstraint",
            ili_name=constraint_name if constraint_name else "PlausibilityConstraint",
            percentage=percentage,
            direction=direction,
            logical_expression=expression,
            scope=ConstraintScope.CLASS,
        )
        
        self._log(f"    ✓ PlausibilityConstraint: {constraint.ili_name} ({percentage}% {direction})", "CONSTRAINT_OK")
        return constraint
    
    def visitExistenceConstraint(self, ctx):
        """Visite EXISTENCE CONSTRAINT"""
        self._log("  visitExistenceConstraint", "CONSTRAINT")
        
        # Extraire le nom (optionnel)
        constraint_name = self._extract_optional_constraint_name(ctx)
        
        # Extraire les attributPaths (attribute1 REQUIRED IN class.attribute2)
        attribute = None
        required_in = None
        
        if hasattr(ctx, 'attributePath'):
            attr_paths = ctx.attributePath()
            if attr_paths:
                if not isinstance(attr_paths, list):
                    attr_paths = [attr_paths]
                
                if len(attr_paths) >= 1:
                    attribute = self._getText(attr_paths[0])
                if len(attr_paths) >= 2:
                    required_in = self._getText(attr_paths[1])
        
        constraint = ExistenceConstraint(
            name=constraint_name if constraint_name else "ExistenceConstraint",
            ili_name=constraint_name if constraint_name else "ExistenceConstraint",
            attribute=attribute,
            required_in=required_in,
            scope=ConstraintScope.ATTRIBUTE,
        )
        
        self._log(f"    ✓ ExistenceConstraint: {constraint.ili_name} ({attribute} in {required_in})", "CONSTRAINT_OK")
        return constraint
    
    def visitUniquenessConstraint(self, ctx):
        """Visite UNIQUE ..."""
        self._log("  visitUniquenessConstraint", "CONSTRAINT")
        
        # Extraire le nom (optionnel)
        constraint_name = self._extract_optional_constraint_name(ctx)
        
        # Déterminer si LOCAL ou BASKET
        local = False
        if hasattr(ctx, 'LOCAL') and ctx.LOCAL():
            local = True
        elif hasattr(ctx, 'BASKET') and ctx.BASKET():
            local = True
        
        # Extraire les attributs uniques
        attributes = []
        
        # Les attributs sont dans globalUniqueness/localUniqueness qui contiennent uniqueEl
        if hasattr(ctx, 'globalUniqueness'):
            global_uniq = ctx.globalUniqueness()
            if global_uniq:
                if not isinstance(global_uniq, list):
                    global_uniq = [global_uniq]
                for gu in global_uniq:
                    if hasattr(gu, 'uniqueEl'):
                        unique_els = gu.uniqueEl()
                        if unique_els:
                            if not isinstance(unique_els, list):
                                unique_els = [unique_els]
                            for ue in unique_els:
                                attr_text = self._getText(ue)
                                if attr_text:
                                    attributes.append(attr_text)
        
        if hasattr(ctx, 'localUniqueness'):
            local_uniq = ctx.localUniqueness()
            if local_uniq:
                if not isinstance(local_uniq, list):
                    local_uniq = [local_uniq]
                for lu in local_uniq:
                    if hasattr(lu, 'uniqueEl'):
                        unique_els = lu.uniqueEl()
                        if unique_els:
                            if not isinstance(unique_els, list):
                                unique_els = [unique_els]
                            for ue in unique_els:
                                attr_text = self._getText(ue)
                                if attr_text:
                                    attributes.append(attr_text)
        
        constraint = UniqueConstraint(
            name=constraint_name if constraint_name else "UniqueConstraint",
            ili_name=constraint_name if constraint_name else "UniqueConstraint",
            local=local,
            attributes=attributes,
            scope=ConstraintScope.CLASS,
        )
        
        self._log(f"    ✓ UniqueConstraint: {constraint.ili_name} ({len(attributes)} attributes, local={local})", "CONSTRAINT_OK")
        return constraint
    
    def visitSetConstraint(self, ctx):
        """Visite SET CONSTRAINT"""
        self._log("  visitSetConstraint", "CONSTRAINT")
        
        # Déterminer la sévérité (GLOBAL / LOCAL / BASKET)
        severity = ConstraintSeverity.ERROR
        if hasattr(ctx, 'LPAR') and ctx.LPAR():
            # Avoir des parenthèses indique une sévérité optionnelle
            pass
        
        # Extraire le nom (optionnel)
        constraint_name = self._extract_optional_constraint_name(ctx)
        
        # Extraire les expressions WHERE et constraint
        where_expr = None
        constraint_expr = None
        
        if hasattr(ctx, 'expression'):
            expressions = ctx.expression()
            if expressions:
                if not isinstance(expressions, list):
                    expressions = [expressions]
                
                # Le premier expression est WHERE (s'il y a WHERE), sinon c'est la contrainte
                if hasattr(ctx, 'WHERE') and ctx.WHERE():
                    if len(expressions) >= 1:
                        where_expr = self.visitExpression(expressions[0])
                    if len(expressions) >= 2:
                        constraint_expr = self.visitExpression(expressions[1])
                else:
                    if len(expressions) >= 1:
                        constraint_expr = self.visitExpression(expressions[0])
        
        constraint = SetConstraint(
            name=constraint_name if constraint_name else "SetConstraint",
            ili_name=constraint_name if constraint_name else "SetConstraint",
            where=where_expr,
            constraint_expression=constraint_expr,
            severity=severity,
            scope=ConstraintScope.GLOBAL,
        )
        
        self._log(f"    ✓ SetConstraint: {constraint.ili_name}", "CONSTRAINT_OK")
        return constraint
    
    def _extract_optional_constraint_name(self, ctx) -> str:
        """Extrait le nom optionnel d'une contrainte (Name COLON)."""
        # Chercher si le premier élément est un Name suivi de COLON
        for i, child in enumerate(ctx.children):
            text = self._getText(child)
            if text and text.isidentifier() and i + 1 < len(ctx.children):
                next_text = self._getText(ctx.children[i + 1])
                if next_text == ":":
                    return text
        return ""
    
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
        """Extrait les éléments d'un TOPIC (classes, domaines, contraintes, etc.)."""
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
            
            elif child_type == "ConstraintsDefContext":
                constraints = self.visit(child)
                if constraints:
                    for constraint in constraints:
                        topic.constraints[constraint.ili_name] = constraint
            
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
                    elif sub_type == "ConstraintsDefContext":
                        constraints = self.visit(sub)
                        if constraints:
                            for constraint in constraints:
                                topic.constraints[constraint.ili_name] = constraint
    
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
    
    def _extract_class_constraints(self, ctx, cls: IliClass):
        """Extrait toutes les contraintes d'une classe."""
        for child in ctx.children:
            if type(child).__name__ == "ConstraintDefContext":
                constraint = self.visit(child)
                if constraint:
                    cls.constraints[constraint.name] = constraint
            
            # Rechercher dans les conteneurs imbriqués
            elif hasattr(child, 'children'):
                for sub in child.children:
                    if type(sub).__name__ == "ConstraintDefContext":
                        constraint = self.visit(sub)
                        if constraint:
                            cls.constraints[constraint.name] = constraint
    
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
