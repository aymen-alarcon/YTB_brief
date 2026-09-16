import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host="postgres",
        port=5432,
        database=os.getenv("METADATA_DATABASE_NAME"),
        user=os.getenv("POSTGRES_CONN_USERNAME"),
        password=os.getenv("POSTGRES_CONN_PASSWORD")
    )


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS youtube_videos CASCADE;
    """)

    cursor.execute("""
        CREATE TABLE youtube_videos (
            video_id VARCHAR(50) PRIMARY KEY,
            channel_id VARCHAR(100),
            channel_title TEXT,
            title TEXT,
            description TEXT,
            published_at TIMESTAMP,
            duration TEXT,
            view_count BIGINT,
            like_count BIGINT,
            comment_count BIGINT
        );
    """)

    conn.commit()

    cursor.close()
    conn.close()


def load_videos(videos):
    conn = get_connection()
    cursor = conn.cursor()

    for video in videos:
        snippet = video.get("snippet", {})
        content_details = video.get("contentDetails", {})
        statistics = video.get("statistics", {})

        cursor.execute("""
            INSERT INTO youtube_videos (
                video_id,
                channel_id,
                channel_title,
                title,
                description,
                published_at,
                duration,
                view_count,
                like_count,
                comment_count
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (video_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                view_count = EXCLUDED.view_count,
                like_count = EXCLUDED.like_count,
                comment_count = EXCLUDED.comment_count;
        """, (
            video["id"],
            snippet.get("channelId"),
            snippet.get("channelTitle"),
            snippet.get("title"),
            snippet.get("description"),
            snippet.get("publishedAt"),
            content_details.get("duration"),
            int(statistics.get("viewCount", 0)),
            int(statistics.get("likeCount", 0)),
            int(statistics.get("commentCount", 0))
        ))

    conn.commit()

    cursor.close()
    conn.close()
