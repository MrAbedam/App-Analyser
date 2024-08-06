import json
import psycopg2
from datetime import datetime
from .redis_client import redis_client
from dateutil.parser import parse as parse_date
def get_db_connection():
    return psycopg2.connect(
        dbname="my_db",
        user="postgres",
        password="1234",
        host="localhost"
    )

def insert_extracted_data(package_name: str):
    try:
        # Fetch app data from Redis
        cached_app_data = redis_client.get(f"{package_name}:app_data")
        if cached_app_data:
            app_data = json.loads(cached_app_data)

            updated = app_data.get('updated', None)
            if updated:
                updated = parse_date(updated) if isinstance(updated, str) else datetime.utcfromtimestamp(updated)
            else:
                updated = None

            conn = get_db_connection()
            cur = conn.cursor()

            print("HOLT SHOT SQP IS FLASFASKLFM")
            insert_sql = """
            INSERT INTO extracted_data (application_id, min_download, score, ratings, reviews, updated, version, ad_supported, timestamp)
            VALUES ((SELECT id FROM applications WHERE package_name=%s), %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (application_id) DO UPDATE
            SET min_download = EXCLUDED.min_download, 
                score = EXCLUDED.score,
                ratings = EXCLUDED.ratings,
                reviews = EXCLUDED.reviews,
                updated = EXCLUDED.updated,
                version = EXCLUDED.version,
                ad_supported = EXCLUDED.ad_supported,
                timestamp = EXCLUDED.timestamp
            """
            cur.execute(insert_sql, (
                package_name,
                app_data.get('minInstalls', 0),
                app_data.get('score', 0.0),
                app_data.get('ratings', 0),
                app_data.get('reviews', 0),
                updated,
                app_data.get('version', ''),
                app_data.get('adSupported', False),
                datetime.utcnow()
            ))
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            print(f"Inserted data for package: {package_name}")

        # Fetch review data from Redis
        cached_review_data = redis_client.get(f"{package_name}:reviews")
        if cached_review_data:
            review_data = json.loads(cached_review_data)

            # Database connection
            conn = get_db_connection()
            cur = conn.cursor()

            # Insert data into reviews table
            for review in review_data:
                insert_review_sql = """
                INSERT INTO reviews (application_id, review_id, at, user_name, thumbs_up_count, score, content, timestamp)
                VALUES ((SELECT id FROM applications WHERE package_name=%s), %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id) DO UPDATE
                SET at = EXCLUDED.at,
                    user_name = EXCLUDED.user_name,
                    thumbs_up_count = EXCLUDED.thumbs_up_count,
                    score = EXCLUDED.score,
                    content = EXCLUDED.content
                """
                cur.execute(insert_review_sql, (
                    package_name,
                    review.get('reviewId', ''),
                    review.get('at', datetime.utcnow()),
                    review.get('userName', ''),
                    review.get('thumbsUpCount', 0),
                    review.get('score', 0),
                    review.get('content', ''),
                    datetime.utcnow()
                ))
            conn.commit()

            # Close the cursor and connection
            cur.close()
            conn.close()

            print(f"Inserted reviews for package: {package_name}")

    except Exception as e:
        print(f"Error inserting data for {package_name}: {str(e)}")

# Function to process packages from Redis
def process_packages():
    package_keys = redis_client.keys('*:app_data')
    for package_key in package_keys:
        package_name = package_key.split(':')[0]
        insert_extracted_data(package_name)
