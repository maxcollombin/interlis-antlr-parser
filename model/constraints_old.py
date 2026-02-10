from pydantic import BaseModel, Field
from typing import List, Optional
from .core import MetaElement

class Constraint(MetaElement):
    pass

class SimpleConstraint(Constraint):
    kind: Optional[str] = None
    percentage: Optional[float] = None
    logical_expression: Optional[str] = None

class ExistenceConstraint(Constraint):
    attr: Optional[str] = None

class UniqueConstraint(Constraint):
    where: List[str] = Field(default_factory=list)
    kind: Optional[str] = None
    unique_def: List[str] = Field(default_factory=list)

class SetConstraint(Constraint):
    where: List[str] = Field(default_factory=list)
    constraint: Optional[str] = None
