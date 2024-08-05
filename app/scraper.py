from fastapi import HTTPException
from google_play_scraper import app, reviews
from .redis_client import redis_client

def fetch_app_data(package_name: str):
    try:
        result = app(package_name)
        # Verify result is a dictionary
        if not isinstance(result, dict):
            raise ValueError("Expected dictionary from app() function")
        app_data = {
            'minInstalls': result['minInstalls'],
            'score': result['score'],
            'ratings': result['ratings'],
            'reviews': result['reviews'],
            'updated': result['updated'],
            'version': result['version'],
            'adSupported': result['adSupported'],
        }
        print(app_data)
        return app_data
    except Exception as e:
        print(f"Error fetching app data for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"App data not found for package: {package_name}")

def fetch_reviews(package_name: str, count: int = 10):
    review_data = []
    for review in reviews(package_name, count=count):
        review_data.append({
            'reviewId': review['reviewId'],
            'at': review['at'],
            'userName': review['userName'],
            'thumbsUpCount': review['thumbsUpCount'],
            'score': review['score'],
            'content': review['content'],
        })
    return review_data

def store_in_redis(app_id: str, app_data: dict, review_data: list):
    redis_client.set(f"{app_id}:app_data", app_data)
    redis_client.set(f"{app_id}:reviews", review_data)
