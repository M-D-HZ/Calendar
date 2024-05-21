CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    public BOOLEAN NOT NULL,
    organizer TEXT NOT NULL
)