from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from . import models, schemas

def get_application(db: Session, app_id: int):
    return db.query(models.Application).filter(models.Application.id == app_id).first()

def get_applications(db: Session):
    return db.query(models.Application).all()

def create_application(db: Session, app: schemas.ApplicationCreate):
    db_app = models.Application(name=app.name, category=app.category)
    if db.query(models.Application).filter(models.Application.name == app.name).first():
        raise HTTPException(status_code=404, detail="Another app with this name already exists in database")
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def update_application(db: Session, app_id: int, app_data: schemas.ApplicationCreate):
    db_app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if db_app:
        db_app.name = app_data.name
        db_app.category = app_data.category
        db.commit()
        db.refresh(db_app)
    return db_app

def delete_application(db: Session, app_id: int):
    db_app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if db_app:
        db.delete(db_app)
        db.commit()
    return db_app

# def truncate_and_reset_table(db: Session):
#     try:
#         db.execute(text("TRUNCATE TABLE applications RESTART IDENTITY CASCADE;"))
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         print(f"Error truncating table: {e}")
#         raise


def get_names(db: Session):
    return db.query(models.Application.name).all()