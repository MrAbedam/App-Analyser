from fastapi import HTTPException
from google_play_scraper import app, reviews
from .redis_client import redis_client
from datetime import datetime
import json


def fetch_app_data(package_name: str):
    try:
        cached_data = redis_client.get(f"{package_name}:app_data")
        if cached_data:
            return json.loads(cached_data)

        result = app(package_name)

        if not isinstance(result, dict) or not result:
            print(f"No app data found or invalid response for package: {package_name}")
            return {}

        app_data = {
            'minInstalls': result.get('minInstalls', 0),
            'score': result.get('score', 0.0),
            'ratings': result.get('ratings', 0),
            'reviews': result.get('reviews', 0),
            'updated': result.get('updated', ''),
            'version': result.get('version', ''),
            'adSupported': result.get('adSupported', False),
        }

        if isinstance(app_data['updated'], datetime):
            app_data['updated'] = app_data['updated'].strftime('%Y-%m-%d %H:%M:%S')

        if app_data:
            redis_client.set(f"{package_name}:app_data", json.dumps(app_data))
        else:
            print(f"No valid app data to store for package: {package_name}")
        return app_data

    except Exception as e:
        print(f"Error fetching app data for {package_name}: {str(e)}")
        return {}

def fetch_reviews(package_name: str, count: int = 10):
    try:
        cached_reviews = redis_client.get(f"{package_name}:reviews")
        if cached_reviews:
            return json.loads(cached_reviews)

        result, _ = reviews(package_name, count=count)


        if not isinstance(result, list) or not result:
            print(f"No reviews found or invalid response for package: {package_name}")
            return []

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

        # Only store in Redis if we have valid data
        if review_data:
            redis_client.set(f"{package_name}:reviews", json.dumps(review_data))
        else:
            print(f"No valid review data to store for package: {package_name}")
        return review_data

    except Exception as e:
        print(f"Error fetching reviews for {package_name}: {str(e)}")
        return []
def store_in_redis(app_id: str, app_data: dict, review_data: list):
    try:
        redis_client.set(f"{app_id}:app_data", json.dumps(app_data), ex=5)
        redis_client.set(f"{app_id}:reviews", json.dumps(review_data), ex=5)
        print(f"Data for {app_id} stored in Redis.")
    except Exception as e:
        print(f"Error storing data in Redis for {app_id}: {str(e)}")
