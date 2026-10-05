-- 12. Titles of all of movies in which both Jennifer Lawrence and Bradley Cooper starred
SELECT m.title FROM movies m
JOIN stars s ON s.movie_id = m.id
JOIN people p ON s.person_id = p.id
WHERE name = 'Jennifer Lawrence' AND m.title IN (
    SELECT title FROM movies
    JOIN stars ON stars.movie_id = movies.id
    JOIN people ON stars.person_id = people.id
    WHERE name = 'Bradley Cooper'
);
