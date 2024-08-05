from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated
from . import crud, models, schemas
from .database import SessionLocal, engine, init_db
from .scraper import fetch_app_data, fetch_reviews, store_in_redis

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

@app.post("/reset/")
def reset_table(db: db_dependency):
    try:
        crud.truncate_and_reset_table(db)
        return {"detail": "Table truncated and sequence reset"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get("/scrape/")
def scrape_all_app_data(db: Session = Depends(get_db)):
    try:
        package_names = [pkg[0] for pkg in crud.get_package_names(db)]


        for package_name in package_names:
            app_data = fetch_app_data(package_name)
            #review_data = fetch_reviews(package_name)
            #store_in_redis(package_name, app_data, review_data)
            print(f"Data for {package_name} stored in Redis.")

        return {"detail": "All data has been scraped and stored in Redis."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")