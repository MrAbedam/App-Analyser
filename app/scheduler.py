from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .scraper import fetch_reviews, fetch_app_data, store_in_redis
from .database import SessionLocal
from . import crud

scheduler = BackgroundScheduler()

def update_redis_data():
    print(f"Scheduler triggered at {datetime.now()}")
    db: Session = SessionLocal()
    try:
        package_names = [pkg[0] for pkg in crud.get_package_names(db)]
        for package_name in package_names:
            print(f"Fetching reviews for {package_name} at {datetime.now()}")
            fetch_reviews(package_name)
            fetch_app_data(package_name)
            # Store fetched data in Redis
            app_data = fetch_app_data(package_name)
            review_data = fetch_reviews(package_name)
            store_in_redis(package_name, app_data, review_data)
    except Exception as e:
        print(f"Error fetching reviews and app_data for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Review or app data not found for package: {package_name}")
    finally:
        db.close()

# def insert_data_into_postgresql():
#     print(f"Data insertion process triggered at {datetime.now()}")
#     try:
#         process_packages()  # Call the function to process and insert data from Redis to PostgreSQL
#         print("imtrying to insert them")
#     except Exception as e:
#         print(f"Error inserting data into PostgreSQL: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error inserting data into PostgreSQL: {str(e)}")

# Add job to update Redis data
scheduler.add_job(update_redis_data, IntervalTrigger(seconds=3600), id='update_redis_data_job', name='Update redis_data every hour')

# # Add job to insert data into PostgreSQL
# scheduler.add_job(insert_data_into_postgresql, IntervalTrigger(seconds=10), id='insert_data_postgresql_job', name='Insert data into PostgreSQL every 30sec')

scheduler.start()
