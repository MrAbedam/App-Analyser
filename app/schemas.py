# project/app/schemas.py

from pydantic import BaseModel
from typing import Optional

class Application(BaseModel):
    id: Optional[int] = None
    name: str