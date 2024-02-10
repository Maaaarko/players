INSERT_PLAYER_INFO = """
INSERT INTO players (id, uri, name, full_name, date_of_birth, age, place_of_birth, country_of_birth, positions, current_club, national_team, appearances_in_current_club, goals_in_current_club, last_updated)
VALUES (%(id)s, %(url)s, %(name)s, %(full_name)s, %(date_of_birth)s, %(age)s, %(place_of_birth)s, %(country_of_birth)s, %(positions)s, %(current_club)s, %(national_team)s, %(appearances_in_current_club)s, %(goals_in_current_club)s, %(timestamp)s)
ON CONFLICT (uri) DO UPDATE
SET id = EXCLUDED.id,
    name = EXCLUDED.name,
    full_name = EXCLUDED.full_name,
    date_of_birth = EXCLUDED.date_of_birth,
    age = EXCLUDED.age,
    place_of_birth = EXCLUDED.place_of_birth,
    country_of_birth = EXCLUDED.country_of_birth,
    positions = EXCLUDED.positions,
    current_club = EXCLUDED.current_club,
    national_team = EXCLUDED.national_team,
    appearances_in_current_club = EXCLUDED.appearances_in_current_club,
    goals_in_current_club = EXCLUDED.goals_in_current_club,
    last_updated = EXCLUDED.last_updated;
"""
