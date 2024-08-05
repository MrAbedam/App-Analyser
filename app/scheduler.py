from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

from fastapi import HTTPException

from .scraper import fetch_reviews, fetch_app_data
from .database import SessionLocal
from . import crud

scheduler = BackgroundScheduler()

def update_redis_data():
    print(f"Scheduler triggered at {datetime.now()}")
    db = SessionLocal()
    try:
        package_names = [pkg[0] for pkg in crud.get_package_names(db)]
        for package_name in package_names:
            print(f"Fetching reviews for {package_name} at {datetime.now()}")
            fetch_reviews(package_name)
            fetch_app_data(package_name)
    except Exception as e:
        print(f"Error fetching reviews and app_data for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Review or app data not found for package: {package_name}")
    finally:
        db.close()

scheduler.add_job(update_redis_data, IntervalTrigger(seconds=3600), id='update_redis_data_job', name='Update redis_data every hour')
scheduler.start()