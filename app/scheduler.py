from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .consumer import process_data_from_redis
from .scraper import fetch_reviews, fetch_app_data, store_in_redis
from .database import SessionLocal
from . import crud

scheduler = BackgroundScheduler()

def update_redis_data():
    print(f"Scheduler triggered at {datetime.now()}")
    db: Session = SessionLocal()
    try:
        names = [pkg[0] for pkg in crud.get_names(db)]
        for name in names:
            print(f"Fetching reviews for {name} at {datetime.now()}")
            fetch_reviews(name)
            fetch_app_data(name)
            # Store fetched data in Redis
            app_data = fetch_app_data(name)
            review_data = fetch_reviews(name)
            store_in_redis(name, app_data, review_data)
        #tabbed one back
        process_data_from_redis()
    except Exception as e:
        print(f"Error fetching reviews and app_data for {name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Review or app data not found for app: {name}")
    finally:
        db.close()


scheduler.add_job(update_redis_data, IntervalTrigger(seconds=3600), id='update_redis_data_job', name='Update redis_data every hour')

def start_scheduler():
    scheduler.start()
    print("Scheduler started.")
