CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS players (
    id UUID PRIMARY KEY,
    uri TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    full_name TEXT NOT NULL,
    dob DATE,
    age INT,
    place_of_birth TEXT,
    country_of_birth TEXT,
    positions TEXT[],
    current_club TEXT,
    national_team TEXT,
    appearances_in_current_club INT,
    goals_in_current_club INT,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
