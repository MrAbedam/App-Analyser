# project/app/models.py


from typing import Optional
from pydantic import BaseModel

#TODO: set correct parameters
class Application(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
