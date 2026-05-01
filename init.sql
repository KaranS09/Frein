-- Initialize PostgreSQL database schema for events

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    date TEXT,
    time TEXT,
    description TEXT,
    type TEXT,
    location TEXT,
    registration_link TEXT,
    estimated_duration TEXT,
    genre TEXT,
    age_limit TEXT,
    language TEXT,
    page_link TEXT,
    poster_link TEXT,
    price TEXT,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, date, time, location)
);

CREATE INDEX IF NOT EXISTS idx_events_location ON events(location);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
