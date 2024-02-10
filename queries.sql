ALTER TABLE players ADD COLUMN IF NOT EXISTS age_category TEXT;
ALTER TABLE players ADD COLUMN IF NOT EXISTS goals_per_club_game REAL;


-- 1.
UPDATE players SET age_category = 'Young' WHERE age <= 23;
UPDATE players SET age_category = 'MidAge' WHERE age > 23 AND age < 33;
UPDATE players SET age_category = 'Old' WHERE age >= 33;

UPDATE players SET goals_per_club_game = goals_in_current_club::REAL / appearances_in_current_club WHERE appearances_in_current_club > 0;


-- 2.
SELECT current_club, AVG(age) AS average_age, AVG(appearances_in_current_club) as average_appearances, COUNT(*) as total_players 
FROM players
WHERE current_club IS NOT NULL
GROUP BY current_club
ORDER BY total_players DESC, average_age DESC, average_appearances DESC;


-- 3.
SELECT players.name, COUNT(p2.name) younger_players_with_more_appearances
FROM players
JOIN players AS p2 ON players.id != p2.id
WHERE players.current_club = 'Barcelona' AND players.age > p2.age AND players.id != p2.id AND players.positions && p2.positions AND p2.appearances_in_current_club > players.appearances_in_current_club
GROUP BY players.name;