import json
import psycopg2
from datetime import datetime

from fastapi import HTTPException

from .redis_client import redis_client
def get_db_connection():
    return psycopg2.connect(
        dbname="my_db",
        user="postgres",
        password="1234",
        host="localhost"
    )

def insert_all_data(name: str):
    try:

        cached_app_data = redis_client.get(f"{name}:app_data")
        if cached_app_data:
            app_data = json.loads(cached_app_data)



            conn = get_db_connection()
            cur = conn.cursor()
            # TODO: add update to fields
            insert_sql = """
            INSERT INTO extracted_data (application_id, min_download, score, ratings, reviews, version, ad_supported, timestamp)
            VALUES ((SELECT id FROM applications WHERE name=%s), %s, %s, %s, %s, %s, %s, %s)
            """

            # ON CONFLICT (application_id) DO UPDATE
            # min_download = EXCLUDED.min_download,
            # score = EXCLUDED.score,
            # ratings = EXCLUDED.ratings,
            # reviews = EXCLUDED.reviews,
            # version = EXCLUDED.version,
            # ad_supported = EXCLUDED.ad_supported,
            # timestamp = EXCLUDED.timestamp

            cur.execute(insert_sql, (
                name,
                app_data.get('minInstalls', 0),
                app_data.get('score', 0.0),
                app_data.get('ratings', 0),
                app_data.get('reviews', 0),
                app_data.get('version', ''),
                app_data.get('adSupported', False),
                datetime.utcnow()
            ))
            conn.commit()

            cur.close()
            conn.close()

            print(f"Inserted data for app: {name}")


        cached_review_data = redis_client.get(f"{name}:reviews")

        if cached_review_data:
            review_data = json.loads(cached_review_data)


            conn = get_db_connection()
            cur = conn.cursor()


            for review in review_data:
                insert_review_sql = """
                INSERT INTO reviews (application_id, review_id, at, user_name, thumbs_up_count, score, content, timestamp)
                VALUES ((SELECT id FROM applications WHERE name=%s), %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (review_id) DO UPDATE
                SET at = EXCLUDED.at,
                    user_name = EXCLUDED.user_name,
                    thumbs_up_count = EXCLUDED.thumbs_up_count,
                    score = EXCLUDED.score,
                    content = EXCLUDED.content
                """
                cur.execute(insert_review_sql, (
                    name,
                    review.get('reviewId', ''),
                    review.get('at', datetime.utcnow()),
                    review.get('userName', ''),
                    review.get('thumbsUpCount', 0),
                    review.get('score', 0),
                    review.get('content', ''),
                    datetime.utcnow()
                ))
            conn.commit()


            cur.close()
            conn.close()

            print(f"Inserted reviews for app: {name}")

    except Exception as e:
        print(f"Error inserting data for {name}: {str(e)}")

def process_apps():
    app_keys = redis_client.keys('*:app_data')
    for app_key in app_keys:
        app_name = app_key.split(':')[0]
        insert_all_data(app_name)

def process_data_from_redis():
    try:
        process_apps()
        return {"detail": "Data has been processed from Redis to PostgreSQL."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing data: {str(e)}")