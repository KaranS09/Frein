import os
import sys
import time

import pandas as pd
import psycopg2

CSV_PATH = "LLM/events.csv"


def get_connection():
    database_url = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
    sslmode = os.getenv("DB_SSLMODE", "require")

    if database_url:
        return psycopg2.connect(database_url, sslmode=sslmode)

    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "events_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "140703")

    return psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        sslmode=sslmode,
    )


def ensure_events_schema(cursor):
    # Keep the old compatibility behavior when the target DB allows it, but do not
    # fail the sync if the hosted database blocks schema changes.
    try:
        cursor.execute(
            """
            ALTER TABLE events
            ALTER COLUMN name TYPE TEXT,
            ALTER COLUMN date TYPE TEXT,
            ALTER COLUMN time TYPE TEXT,
            ALTER COLUMN description TYPE TEXT,
            ALTER COLUMN type TYPE TEXT,
            ALTER COLUMN location TYPE TEXT,
            ALTER COLUMN registration_link TYPE TEXT,
            ALTER COLUMN estimated_duration TYPE TEXT,
            ALTER COLUMN genre TYPE TEXT,
            ALTER COLUMN age_limit TYPE TEXT,
            ALTER COLUMN language TYPE TEXT,
            ALTER COLUMN page_link TYPE TEXT,
            ALTER COLUMN poster_link TYPE TEXT,
            ALTER COLUMN price TYPE TEXT,
            ALTER COLUMN status TYPE TEXT;
            """
        )
    except psycopg2.Error as exc:
        print(f"Skipping schema ensure step: {exc}")
        cursor.connection.rollback()


def wait_for_database(max_attempts=30, delay_seconds=2):
    for attempt in range(1, max_attempts + 1):
        try:
            conn = get_connection()
            conn.close()
            print("Database connection established.")
            return
        except psycopg2.Error as exc:
            print(f"Database not ready yet (attempt {attempt}/{max_attempts}): {exc}")
            time.sleep(delay_seconds)

    raise RuntimeError("Timed out waiting for database connection.")


def insert_events():
    df = pd.read_csv(CSV_PATH)

    conn = get_connection()
    cur = conn.cursor()

    ensure_events_schema(cur)

    # Insert query with conflict handling
    query = """
    INSERT INTO events (
        name, date, time, description, type, location,
        registration_link, estimated_duration,
        genre, age_limit, language, page_link, poster_link,
        price, status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (name, date, time, location) DO NOTHING;
    """

    for _, row in df.iterrows():
        cur.execute(
            query,
            (
                row["Name of the event"],
                row["Date"],
                row["Time"],
                row["Event description"],
                row["Type of event"],
                row["Location (Bangalore only)"],
                row["Registration Link"],
                row["Estimated duration"],
                row["Genre"],
                row["Age Limit"],
                row["Language"],
                row["Page Link"],
                row["Poster Link"],
                row["Price"],
                row["Status"],
            ),
        )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    if "--wait-for-db" in sys.argv:
        wait_for_database()
    else:
        insert_events()
