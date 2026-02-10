from pydantic import BaseModel, Field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .attributes import Attribute

class DocText(BaseModel):
    name: str
    text: str

class MetaElement(BaseModel):
    name: str
    documentation: List[DocText] = Field(default_factory=list)

class ExtendableME(MetaElement):
    abstract: bool = False
    generic: bool = False
    final: bool = False

class Package(MetaElement):
    pass

class Model(Package):
    ili_version: str = ""
    contracted: bool = False
    kind: str = ""
    language: str = ""
    at: str = ""
    version: str = ""
    no_incremental_transfer: bool = False
    charset_iana_name: str = ""
    xmlns: str = ""
    submodels: List['SubModel'] = Field(default_factory=list)
    topics: List['Topic'] = Field(default_factory=list)
    # TODO: ili1_transfername, ili1_format, meta_attributes, etc.

class SubModel(Package):
    # Peut contenir des classes, contraintes, etc.
    classes: List['Class'] = Field(default_factory=list)
    constraints: List = Field(default_factory=list)
    # TODO: autres éléments (DataUnit, etc.)

class Topic(BaseModel):
    name: str
    classes: List['Class'] = Field(default_factory=list)
    # TODO: autres éléments (associations, etc.)

class Class(ExtendableME):
    kind: str = "Class"
    multiplicity: Optional[str] = None
    embedded_role_transfer: bool = False
    ili1_optional_table: bool = False
    attributes: List['Attribute'] = Field(default_factory=list)
    base: Optional['Class'] = None
    # TODO: constraints, meta_attributes, etc.

from .attributes import Attribute
Class.model_rebuild()
