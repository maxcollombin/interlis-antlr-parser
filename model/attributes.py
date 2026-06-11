from pydantic import BaseModel, Field
from typing import List, Optional

from .types import DomainType


class Attribute(BaseModel):
    name: str
    type_: DomainType
    mandatory: bool = False


class MetaAttribute(Attribute):
    value: Optional[str] = None


class Role(Attribute):
    strongness: Optional[str] = None
    ordered: bool = False
    multiplicity: Optional[str] = None
    derivates: List[str] = Field(default_factory=list)
    embedded_transfer: bool = False
