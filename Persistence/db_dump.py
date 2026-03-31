import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv("LLM/events.csv")

# Connect to Postgres
conn = psycopg2.connect(
    dbname="events_db",
    user="postgres",
    password="140703",
    host="localhost",
    port="5432"
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