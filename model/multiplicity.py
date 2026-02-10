from pydantic import BaseModel
from typing import Optional

class Multiplicity(BaseModel):
    minimum: int
    maximum: Optional[int] = None
