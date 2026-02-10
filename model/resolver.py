"""
Resolver INTERLIS : résolution sémantique après parsing AST.

Responsabilités :
- Construire les index de classes/domaines
- Résoudre les références croisées
- Valider la cohérence du modèle
- Enrichir l'AST avec des métadonnées résolues
"""

from typing import Dict, Optional
from model.metamodel import IliModel, IliTopic, IliClass, IliDomain, IliAssociation


class IliResolver:
    """Résout et valide un modèle INTERLIS après parsing."""
    
    def __init__(self, model: IliModel):
        self.model = model
    
    def resolve(self) -> IliModel:
        """Exécute la résolution complète du modèle."""
        self._build_indices()
        self._resolve_inheritance()
        self._resolve_domain_references()
        self._resolve_association_references()
        return self.model
    
    def _build_indices(self) -> None:
        """Construit les index pour accès rapide."""
        for topic in self.model.topics.values():
            for cls in topic.classes.values():
                self.model._classes_index[cls.ili_name] = cls
            for domain in topic.domains.values():
                self.model._domains_index[domain.ili_name] = domain
    
    def _resolve_inheritance(self) -> None:
        """Résout les relations d'héritage entre classes."""
        for topic in self.model.topics.values():
            for cls in topic.classes.values():
                # Ici, implémenter la logique pour résoudre base_class si elle est stockée par nom
                pass
    
    def _resolve_domain_references(self) -> None:
        """Résout les références de domaines dans les attributs."""
        for topic in self.model.topics.values():
            for cls in topic.classes.values():
                for attr in cls.attributes.values():
                    if attr.domain and attr.domain.ili_name:
                        resolved_domain = self.model.resolve_domain(attr.domain.ili_name)
                        if resolved_domain:
                            attr.domain = resolved_domain
    
    def _resolve_association_references(self) -> None:
        """Résout les références de classes dans les associations."""
        for topic in self.model.topics.values():
            for assoc in topic.associations.values():
                # Résoudre les targets des rôles
                if assoc.role_a.target_class and hasattr(assoc.role_a.target_class, 'ili_name'):
                    if isinstance(assoc.role_a.target_class, str):
                        assoc.role_a.target_class = self.model.resolve_class(assoc.role_a.target_class)
                if assoc.role_b.target_class and hasattr(assoc.role_b.target_class, 'ili_name'):
                    if isinstance(assoc.role_b.target_class, str):
                        assoc.role_b.target_class = self.model.resolve_class(assoc.role_b.target_class)
