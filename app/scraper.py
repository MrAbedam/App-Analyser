from fastapi import HTTPException
from google_play_scraper import app, reviews
from .redis_client import redis_client
from datetime import datetime
import json

# Sentinel value for no data
NO_DATA_SENTINEL = "NO_DATA"

def fetch_app_data(package_name: str):
    try:
        # Check if data is already in Redis
        cached_data = redis_client.get(f"{package_name}:app_data")
        if cached_data:
            return json.loads(cached_data)

        # Fetch data from API if not cached
        result = app(package_name)
        if not isinstance(result, dict):
            raise ValueError("Expected dictionary from app() function")

        app_data = {
            'minInstalls': result.get('minInstalls', 0),
            'score': result.get('score', 0.0),
            'ratings': result.get('ratings', 0),
            'reviews': result.get('reviews', 0),
            'updated': result.get('updated', ''),
            'version': result.get('version', ''),
            'adSupported': result.get('adSupported', False),
        }

        # Convert 'updated' to string if it's a datetime object
        if isinstance(app_data['updated'], datetime):
            app_data['updated'] = app_data['updated'].strftime('%Y-%m-%d %H:%M:%S')

        # Store in Redis and return
        redis_client.set(f"{package_name}:app_data", json.dumps(app_data))
        return app_data
    except Exception as e:
        print(f"Error fetching app data for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"App data not found for package: {package_name}")

def fetch_reviews(package_name: str, count: int = 10):
    try:
        cached_reviews = redis_client.get(f"{package_name}:reviews")
        if cached_reviews:
            return json.loads(cached_reviews)

        # Fetch reviews from API if not cached
        result, _ = reviews(package_name, count=count)
        if not isinstance(result, list):
            raise ValueError("Expected list from reviews() function")

        review_data = []
        for review in result:
            review_data.append({
                'reviewId': review.get('reviewId', ''),
                'at': review.get('at', datetime.now()).strftime('%Y-%m-%d %H:%M:%S') if isinstance(
                    review.get('at', datetime.now()), datetime) else review.get('at', ''),
                'userName': review.get('userName', ''),
                'thumbsUpCount': review.get('thumbsUpCount', 0),
                'score': review.get('score', 0),
                'content': review.get('content', ''),
            })

        # Store in Redis and return
        redis_client.set(f"{package_name}:reviews", json.dumps(review_data))
        return review_data
    except Exception as e:
        print(f"Error fetching reviews for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Review data not found for package: {package_name}")

def store_in_redis(app_id: str, app_data: dict, review_data: list):
    try:
        redis_client.set(f"{app_id}:app_data", json.dumps(app_data), ex=100)
        redis_client.set(f"{app_id}:reviews", json.dumps(review_data), ex=100)
        print(f"Data for {app_id} stored in Redis.")
    except Exception as e:
        print(f"Error storing data in Redis for {app_id}: {str(e)}")
