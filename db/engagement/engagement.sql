CREATE TYPE engagement_status AS ENUM ('pending', 'accepted', 'rejected', 'maybe');

CREATE TABLE engagement (
    id SERIAL PRIMARY KEY,
    "user" TEXT NOT NULL,
    event_id INT NOT NULL,
    invite_status engagement_status NOT NULL DEFAULT 'pending'
)