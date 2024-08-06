
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    package_name = Column(String, index=True)

    extracted_data = relationship("ExtractedData", back_populates="application")
    reviews = relationship("Review", back_populates="application")

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    min_download = Column(Integer, index=True)
    score = Column(Float)
    ratings = Column(Integer)
    reviews = Column(Integer)
    updated = Column(DateTime)
    version = Column(String)
    ad_supported = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="extracted_data")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    review_id = Column(String, unique=True, index=True)
    at = Column(DateTime)
    user_name = Column(String)
    thumbs_up_count = Column(Integer)
    score = Column(Integer)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="reviews")
