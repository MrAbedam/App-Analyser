from pydantic import BaseModel

class ApplicationBase(BaseModel):
    name: str
    category : str

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int

    class Config:
        orm_mode = True
