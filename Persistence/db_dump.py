import pandas as pd
import psycopg2
import os

# Load CSV
df = pd.read_csv("LLM/events.csv")

# Get database credentials from environment variables or use defaults
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "events_db")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "140703")

# Connect to Postgres
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)

cur = conn.cursor()

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

# Insert rows
for _, row in df.iterrows():
    cur.execute(query, (
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
        row["Status"]
    ))

conn.commit()
cur.close()
conn.close()