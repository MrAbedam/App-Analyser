from sqlalchemy.orm import Session
from . import models, schemas

def get_application(db: Session, app_id: int):
    return db.query(models.Application).filter(models.Application.id == app_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Application).offset(skip).limit(limit).all()

def create_application(db: Session, app: schemas.ApplicationCreate):
    db_app = models.Application(name=app.name)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def update_application(db: Session, app_id: int, app_data: schemas.ApplicationCreate):
    db_app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if db_app:
        db_app.name = app_data.name
        db.commit()
        db.refresh(db_app)
    return db_app

def delete_application(db: Session, app_id: int):
    db_app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if db_app:
        db.delete(db_app)
        db.commit()
    return db_app
