from sqlalchemy import Column, Integer, String
from .database import Base


class Application(Base):

    #application list
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    package_name = Column(String, index=True)

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    min_download = Column(Integer, index = True)