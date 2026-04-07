-- Initialize PostgreSQL database schema for events

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date VARCHAR(100),
    time VARCHAR(100),
    description TEXT,
    type VARCHAR(100),
    location VARCHAR(255),
    registration_link VARCHAR(500),
    estimated_duration VARCHAR(100),
    genre VARCHAR(100),
    age_limit VARCHAR(50),
    language VARCHAR(100),
    page_link VARCHAR(500),
    poster_link VARCHAR(500),
    price VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, date, time, location)
);

CREATE INDEX IF NOT EXISTS idx_events_location ON events(location);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
