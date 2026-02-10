from pydantic import BaseModel, Field
from typing import List, Optional
from .types import Type
from .core import MetaElement

class DomainType(Type):
    mandatory: bool = False
    constraints: List['DomainConstraint'] = Field(default_factory=list)

class DomainConstraint(MetaElement):
    expression: Optional[str] = None
