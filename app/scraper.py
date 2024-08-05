from fastapi import HTTPException
from google_play_scraper import app, reviews
from .redis_client import redis_client
from datetime import datetime
import json


def fetch_app_data(package_name: str):
    try:
        result = app(package_name)
        # Verify result is a dictionary
        if not isinstance(result, dict):
            raise ValueError("Expected dictionary from app() function")

        app_data = {
            'minInstalls': result.get('minInstalls', 0),
            'score': result.get('score', 0.0),
            'ratings': result.get('ratings', 0),
            'reviews': result.get('reviews', 0),
            'updated': result.get('updated', None),
            'version': result.get('version', ''),
            'adSupported': result.get('adSupported', False),
        }

        # Ensure updated is in string format if it's a datetime object
        if isinstance(app_data['updated'], datetime):
            app_data['updated'] = app_data['updated'].strftime('%Y-%m-%d %H:%M:%S')
        #
        print("APP_DATA:")
        print(app_data)
        return app_data
    except Exception as e:
        print(f"Error fetching app data for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"App data not found for package: {package_name}")


def fetch_reviews(package_name: str, count: int = 3):#set count to 1000 later
    try:
        review_data = []
        result, _ = reviews(package_name, count=count)

        # Verify result is a list of dictionaries
        if not isinstance(result, list):
            raise ValueError("Expected list from reviews() function")

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
        print("REVIEWS:")
        print (review_data)
        return review_data
    except Exception as e:
        print(f"Error fetching reviews for {package_name}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Review data not found for package: {package_name}")


def store_in_redis(app_id: str, app_data: dict, review_data: list):
    print("STORING APP_DATA and REVIEWS IN REDIS")
    try:
        redis_client.set(f"{app_id}:app_data", json.dumps(app_data))
        redis_client.set(f"{app_id}:reviews", json.dumps(review_data))
        print(f"Data for {app_id} stored in Redis.")
    except Exception as e:
        print(f"Error storing data in Redis for {app_id}: {str(e)}")