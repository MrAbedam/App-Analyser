
from google_play_scraper import app, reviews, search
from .redis_client import redis_client
from datetime import datetime
import json


def fetch_app_data(name: str):
    try:

        cached_data = redis_client.get(f"{name}:app_data")
        if cached_data:
            return json.loads(cached_data)
        else:
            package_name_res = search(name, n_hits=1)
            result = app(package_name_res[0].get('appId'))

        if not isinstance(result, dict) or not result:
            print(f"No app data found or invalid response for app: {name}")
            return {}


        app_data = {
            'minInstalls': result.get('minInstalls', 0),
            'score': result.get('score', 0.0),
            'ratings': result.get('ratings', 0),
            'reviews': result.get('reviews', 0),
            'updated': result.get('lastUpdatedOn',None),
            'version': result.get('version', ''),
            'adSupported': result.get('adSupported', False),
        }

        if app_data:
            redis_client.set(f"{name}:app_data", json.dumps(app_data))
        else:
            print(f"No valid app data to store for package: {name}")
        return app_data

    except Exception as e:
        print(f"Error fetching app data for {name}: {str(e)}")
        return {}

def fetch_reviews(name: str, count: int = 500):
    try:
        cached_reviews = redis_client.get(f"{name}:reviews")
        if cached_reviews:
            return json.loads(cached_reviews)
        else:
            package_name_res = search(name, n_hits=1)
            package_name = package_name_res[0].get('appId')
            result, _ = reviews(package_name, count=count)


        if not isinstance(result, list) or not result:
            print(f"No reviews found or invalid response for app: {name}")
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

        if review_data:
            redis_client.set(f"{name}:reviews", json.dumps(review_data))
        else:
            print(f"No valid review data to store for app: {name}")
        return review_data

    except Exception as e:
        print(f"Error fetching reviews for {name}: {str(e)}")
        return []

def store_in_redis(app_id: str, app_data: dict, review_data: list):
    try:
        if (not app_data or not review_data):
            print(f"Error storing data in Redis for {app_id}")
            return None
        redis_client.set(f"{app_id}:app_data", json.dumps(app_data), ex=3600)
        redis_client.set(f"{app_id}:reviews", json.dumps(review_data), ex=3600)
        print(f"Data for {app_id} stored in Redis.")
    except Exception as e:
        print(f"Error storing data in Redis for {app_id}: {str(e)}")