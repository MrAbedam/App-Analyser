from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated
from . import crud, models, schemas
from .database import SessionLocal, engine, init_db

models.Base.metadata.create_all(bind=engine)
init_db()
#dorost kardan table ha tu pg

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#connection creation

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/applications/",response_model=schemas.Application)
def create_application(app: schemas.ApplicationCreate, db : db_dependency):
    return crud.create_application(db=db, app=app)

@app.get("/applications/", response_model=List[schemas.Application])
def read_applications(db: Session = Depends(get_db)):
    applications = crud.get_applications(db)
    return applications

@app.put("/applications/{app_id}", response_model=schemas.Application)
def update_application(app_id: int, app: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    db_app = crud.get_application(db, app_id=app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return crud.update_application(db=db, app_id=app_id, app_data=app)

@app.delete("/applications/{app_id}", response_model=schemas.Application)
def delete_application(app_id: int, db: Session = Depends(get_db)):
    db_app = crud.get_application(db, app_id=app_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return crud.delete_application(db=db, app_id=app_id)