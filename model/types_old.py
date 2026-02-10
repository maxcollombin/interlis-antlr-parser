from pydantic import BaseModel, Field
from typing import List, Optional

class Type(BaseModel):
    pass

class TextType(Type):
    kind: str = "TEXT"
    max_length: Optional[int] = None

class NumericType(Type):
    min_: Optional[str] = None
    max_: Optional[str] = None
    circular: bool = False

class EnumType(Type):
    values: List[str] = Field(default_factory=list)

# TODO: BlackboxType, CoordType, FormattedType, BooleanType, etc.
