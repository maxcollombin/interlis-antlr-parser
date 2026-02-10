from pydantic import BaseModel, Field
from typing import List, Optional
from .core import MetaElement
from .types import Type

class Argument(BaseModel):
    name: str
    type_: Optional[Type] = None

class FunctionDef(MetaElement):
    arguments: List[Argument] = Field(default_factory=list)
    result_type: Optional[Type] = None
    # TODO: add body/expressions if needed
